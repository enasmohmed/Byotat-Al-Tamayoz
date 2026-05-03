"""
Receives the same JSON payload that ContactFormView POSTs to ``contact_whatsapp_api_url``.

Use case: set Site settings «Contact WhatsApp API URL» (or ``CONTACT_WHATSAPP_API_URL``)
to ``https://<your-domain>/contact/api/whatsapp/`` so the site calls itself.

Optional: set ``WHATSAPP_CLOUD_*`` env vars to forward ``body`` to Meta WhatsApp Cloud API.
"""

from __future__ import annotations

import json
import logging

import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

META_MSG_MAX = 4096


def _bearer_matches(request) -> bool:
    expected = (getattr(settings, "CONTACT_WHATSAPP_API_TOKEN", "") or "").strip()
    if not expected:
        return False
    auth = (request.headers.get("Authorization") or "").strip()
    if not auth.startswith("Bearer "):
        return False
    return auth[7:].strip() == expected


def _send_whatsapp_cloud(to_digits: str, body: str) -> tuple[bool, str | None]:
    token = (getattr(settings, "WHATSAPP_CLOUD_ACCESS_TOKEN", "") or "").strip()
    phone_id = (getattr(settings, "WHATSAPP_CLOUD_PHONE_NUMBER_ID", "") or "").strip()
    version = (getattr(settings, "WHATSAPP_CLOUD_API_VERSION", "") or "v21.0").strip()

    if not token or not phone_id:
        return True, None

    to_digits = "".join(c for c in str(to_digits or "") if c.isdigit())
    if not to_digits:
        return False, "missing_or_invalid_to"

    text = (body or "")[:META_MSG_MAX]
    url = f"https://graph.facebook.com/{version}/{phone_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to_digits,
        "type": "text",
        "text": {"preview_url": False, "body": text},
    }
    try:
        r = requests.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=20,
        )
        r.raise_for_status()
        return True, None
    except Exception as exc:  # noqa: BLE001
        logger.exception("WhatsApp Cloud API send failed: %s", exc)
        return False, str(exc)


@csrf_exempt
@require_POST
def whatsapp_contact_webhook(request):
    if not _bearer_matches(request):
        return JsonResponse({"ok": False, "error": "unauthorized"}, status=401)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"ok": False, "error": "expected_object"}, status=400)

    ok, err = _send_whatsapp_cloud(payload.get("to") or "", payload.get("body") or "")
    if not ok:
        return JsonResponse({"ok": False, "error": err or "send_failed"}, status=502)

    return JsonResponse({"ok": True})
