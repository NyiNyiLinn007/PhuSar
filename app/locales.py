from __future__ import annotations

from typing import Final


REGION_LABELS: Final[dict[str, dict[str, str]]] = {
    "yangon": {"en": "Yangon", "my": "\u101b\u1014\u103a\u1000\u102f\u1014\u103a"},
    "mandalay": {"en": "Mandalay", "my": "\u1019\u1014\u1039\u1010\u101c\u1031\u1038"},
    "naypyidaw": {"en": "Naypyidaw", "my": "\u1014\u1031\u1015\u103c\u100a\u103a\u1010\u1031\u102c\u103a"},
    "bago": {"en": "Bago", "my": "\u1015\u1032\u1001\u1030\u1038"},
    "ayeyarwady": {"en": "Ayeyarwady", "my": "\u1027\u101b\u102c\u101d\u1010\u102e"},
    "other": {"en": "Other", "my": "\u1021\u1001\u103c\u102c\u1038"},
}

REPORT_REASON_LABELS: Final[dict[str, dict[str, str]]] = {
    "fake": {"en": "Fake account", "my": "\u1021\u1000\u1031\u102c\u1004\u1037\u103a\u1021\u1010\u102f"},
    "spam": {"en": "Spam", "my": "\u1005\u1015\u1019\u103a\u1038"},
    "inappropriate": {"en": "Inappropriate content", "my": "\u1019\u101e\u1004\u1037\u103a\u101c\u103b\u1031\u102c\u103a\u101e\u1031\u102c \u1021\u1000\u103c\u1031\u102c\u1004\u103a\u1038\u1021\u101b\u102c"},
    "abusive": {"en": "Abusive behavior", "my": "\u1021\u1015\u103c\u102f\u1021\u1019\u1030 \u1019\u1000\u1031\u102c\u1004\u103a\u1038"},
}

MESSAGES: Final[dict[str, dict[str, str]]] = {
    "en": {
        "lang_name": "English",
        "welcome": "Welcome to Phu Sar (\u1016\u1030\u1038\u1005\u102c). Start your journey to find your match.",
        "menu_text": "Choose an action:",
        "choose_language": "Choose your language:",
        "ask_name": "Send your display name:",
        "ask_gender": "Select your gender:",
        "ask_seeking": "Who are you looking for?",
        "ask_region": "Pick your region:",
        "ask_location": "Share your current location or select township manually:",
        "ask_location_update": "Share your new GPS location:",
        "ask_township": "Enter your township:",
        "ask_age": "Enter your age (18-99):",
        "ask_bio": "Write a short bio (max 500 chars):",
        "ask_photo": "Upload one clear profile photo:",
        "location_received": "Location received.",
        "location_updated": "Your location was updated.",
        "location_share_required": "Please tap 'Share My Location' and send GPS.",
        "township_from_gps": "Nearby",
        "invalid_age": "Age must be a number between 18 and 99.",
        "invalid_text": "Please send text.",
        "invalid_photo": "Please upload a photo image.",
        "profile_saved": "Your profile is ready.",
        "profile_incomplete": "Complete registration first with /start.",
        "registration_cancelled": "Registration canceled.",
        "delete_account_done": "Your account was deleted. All your photos and matches are now gone.",
        "banned": "Your account is currently banned. Contact support.",
        "no_profiles": "No more profiles for now. Please try again later.",
        "match": "You matched with {name}. \U0001F60D",
        "match_username": "You matched with {username}. \U0001F60D",
        "match_no_username": "You matched, but this user has no Telegram username set yet.",
        "set_username_hint": "Please set a Telegram username in Settings so matches can find you.",
        "like_received": "Someone liked your profile. You can like back from below:",
        "superlike_received": "{name} sent you a SuperLike \U0001F31F",
        "already_premium": "You already have active premium.",
        "premium_disabled": "Premium features are currently disabled.",
        "premium_intro": "Phu Sar Premium gives unlimited likes, See Who Liked You, rewind, and boost.",
        "premium_buy_title": "Buy Premium",
        "premium_choose_plan": "Choose a premium plan:",
        "premium_choose_provider": "Choose payment provider:",
        "premium_plan_weekly": "Weekly (1,500 MMK)",
        "premium_plan_monthly": "Monthly (3,000 MMK)",
        "premium_plan_selected": "Plan selected: {plan}.",
        "premium_payment_details": "Send payment to:\n{phone}\nThen upload your payment screenshot.",
        "premium_send_receipt": "Please upload your KBZPay/WaveMoney screenshot.",
        "premium_submitted": "Payment screenshot submitted. Admin review is pending.",
        "premium_approved": "Your premium status is approved.",
        "premium_rejected": "Your premium request was rejected. Please submit a clearer receipt.",
        "premium_welcome": "Phu Sar Premium is active now. Enjoy unlimited swipes.",
        "liked_you_intro": "People who liked you:",
        "liked_you_empty": "No one liked you yet.",
        "liked_you_locked": "Premium required to see who liked you.",
        "likes_limit_reached": "Daily like limit reached (30). Upgrade to Premium for unlimited likes.",
        "rewind_done": "Last pass was rewound.",
        "rewind_missing": "No recent pass to rewind.",
        "boost_done": "Boost sent. Your profile was pushed to up to 100 nearby users.",
        "boost_locked": "Premium required for Profile Boost.",
        "report_prompt": "Select a reason to report this profile:",
        "report_submitted": "Thanks. Your report was submitted for moderation.",
        "admin_only": "This action is admin-only.",
        "whereami_empty": "No GPS location saved yet.\nRegion/Township: {region}, {township}\nUse /location to update.",
        "whereami_value": (
            "Your saved GPS:\n"
            "Lat: {lat}\n"
            "Lon: {lon}\n"
            "Region/Township: {region}, {township}"
        ),
        "user_banned": "User has been banned.",
        "user_unbanned": "User has been unbanned.",
        "admin_approve_usage": "Usage: /approve <user_id> <days>",
        "admin_reject_usage": "Usage: /reject <user_id>",
        "admin_premium_done": "Premium approved for {days} days.",
        "admin_reject_done": "Premium request rejected.",
        "premium_no_pending": "No pending premium request for this user.",
        "profile_title": "Your profile",
        "label_age": "Age",
        "label_gender": "Gender",
        "label_seeking": "Seeking",
        "label_location": "Location",
        "distance_away": "\U0001F4CD {km} km away",
        "btn_discover": "Discover",
        "btn_premium": "Premium",
        "btn_profile": "My Profile",
        "btn_edit": "Edit Profile",
        "btn_liked_you": "See Who Liked You",
        "btn_boost": "Boost",
        "btn_male": "Male",
        "btn_female": "Female",
        "btn_both": "Both",
        "btn_share_location": "\U0001F4CD Share My Location",
        "btn_township_manual": "\U0001F3D9 Select Township Manually",
        "btn_like": "\u2764\ufe0f",
        "btn_like_back": "\u2764\ufe0f Like Back",
        "btn_pass": "\u274C",
        "btn_superlike": "\U0001F31F Super",
        "btn_rewind": "\U0001F519 Rewind",
        "btn_report": "\U0001F6A9 Report",
        "btn_kbz": "KBZPay",
        "btn_wave": "WaveMoney",
        "btn_cancel": "Cancel",
    },
    "my": {
        "lang_name": "\u1019\u103c\u1014\u103a\u1019\u102c",
        "welcome": "\u1016\u1030\u1038\u1005\u102c (Phu Sar) \u1019\u103e \u1000\u103c\u102d\u102f\u1006\u102d\u102f\u1015\u102b\u101e\u100a\u103a\u104b \u101e\u1004\u1037\u103a\u1016\u1030\u1038\u1005\u102c\u101b\u103e\u1004\u103a\u1000\u102d\u102f \u101b\u103e\u102c\u1016\u103d\u1031\u1016\u102d\u102f\u1037 \u1021\u1031\u102c\u1000\u103a\u1000 \u1001\u101c\u102f\u1010\u103a\u1019\u103b\u102c\u1038\u1010\u103d\u1004\u103a \u101b\u103d\u1031\u1038\u1015\u102b\u104b",
        "menu_text": "\u101c\u102f\u1015\u103a\u1006\u1031\u102c\u1004\u103a\u101b\u1014\u103a \u1010\u1005\u103a\u1001\u102f\u101b\u103d\u1031\u1038\u1015\u102b\u104b",
        "choose_language": "\u1018\u102c\u101e\u102c\u1005\u1000\u102c\u1038 \u101b\u103d\u1031\u1038\u1015\u102b\u104b",
        "ask_name": "\u1015\u103c\u101e\u1019\u100a\u1037\u103a \u1021\u1019\u100a\u103a\u1015\u102d\u102f\u1037\u1015\u102b\u104b",
        "ask_gender": "\u101e\u1004\u1037\u103a\u101c\u102d\u1004\u103a \u101b\u103d\u1031\u1038\u1015\u102b\u104b",
        "ask_seeking": "\u1018\u101a\u103a\u101e\u1030\u1000\u102d\u102f \u101b\u103e\u102c\u1001\u103b\u1004\u103a\u1015\u102b\u101e\u101c\u1032\u104b",
        "ask_region": "\u1010\u102d\u102f\u1004\u103a\u1038\u1012\u1031\u101e\u1000\u103c\u102e\u1038/\u1015\u103c\u100a\u103a\u1014\u101a\u103a \u101b\u103d\u1031\u1038\u1015\u102b\u104b",
        "ask_location": "\u101c\u1000\u103a\u101b\u103e\u102d \u1010\u100a\u103a\u1014\u1031\u101b\u102c\u1000\u102d\u102f \u1019\u103b\u103e\u101d\u1031\u1015\u102b \u101e\u102d\u102f\u1037\u1019\u101f\u102f\u1010\u103a \u1019\u103c\u102d\u102f\u1037\u1014\u101a\u103a\u1000\u102d\u102f \u1000\u102d\u102f\u101a\u103a\u1010\u102d\u102f\u1004\u103a \u101b\u103d\u1031\u1038\u1015\u102b\u104b",
        "ask_location_update": "\u1010\u100a\u103a\u1014\u1031\u101b\u102c\u1021\u101e\u1005\u103a GPS \u1000\u102d\u102f \u1015\u102d\u102f\u1037\u1015\u102b\u104b",
        "ask_township": "\u1019\u103c\u102d\u102f\u1037\u1014\u101a\u103a \u101b\u102d\u102f\u1000\u103a\u1011\u100a\u1037\u103a\u1015\u102b\u104b",
        "ask_age": "\u1021\u101e\u1000\u103a \u1011\u100a\u1037\u103a\u1015\u102b (18-99)\u104b",
        "ask_bio": "\u1021\u1000\u103c\u1031\u102c\u1004\u103a\u1038\u1021\u101b\u102c\u1010\u102d\u102f \u101b\u1031\u1038\u1015\u102b (500 \u1005\u102c\u101c\u102f\u1036\u1038 \u1011\u102d)\u104b",
        "ask_photo": "Profile \u1013\u102c\u1010\u103a\u1015\u102f\u1036 \u1010\u1004\u103a\u1015\u102b\u104b",
        "location_received": "\u1010\u100a\u103a\u1014\u1031\u101b\u102c \u101c\u1000\u103a\u1001\u1036\u101b\u101b\u103e\u102d\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b",
        "location_updated": "\u101e\u1004\u1037\u103a\u1010\u100a\u103a\u1014\u1031\u101b\u102c\u1000\u102d\u102f \u1021\u1015\u103a\u1012\u102d\u1010\u103a\u101c\u102f\u1015\u103a\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b",
        "location_share_required": "\u2018\U0001F4CD Share My Location\u2019 \u1000\u102d\u102f \u1014\u103e\u102d\u1015\u103a\u1015\u103c\u102e\u1038 GPS \u1015\u102d\u102f\u1037\u1015\u102b\u104b",
        "township_from_gps": "\u1021\u1014\u102e\u1038\u1021\u1014\u102c\u1038",
        "invalid_age": "\u1021\u101e\u1000\u103a\u1000\u102d\u102f 18 \u1019\u103e 99 \u1021\u1010\u103d\u1004\u103a\u1038 \u1011\u100a\u1037\u103a\u1015\u102b\u104b",
        "invalid_text": "\u1005\u102c\u101e\u102c\u1038\u1016\u103c\u1004\u1037\u103a \u1015\u102d\u102f\u1037\u1015\u102b\u104b",
        "invalid_photo": "\u1013\u102c\u1010\u103a\u1015\u102f\u1036 \u1016\u102d\u102f\u1004\u103a\u1010\u1004\u103a\u1015\u1031\u1038\u1015\u102b\u104b",
        "profile_saved": "\u101e\u1004\u1037\u103a\u1015\u101b\u102d\u102f\u1016\u102d\u102f\u1004\u103a \u101e\u102d\u1019\u103a\u1038\u1006\u100a\u103a\u1038\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b",
        "profile_incomplete": "/start \u1014\u103e\u1004\u1037\u103a \u1015\u1011\u1019\u1006\u102f\u1036\u1038 \u1019\u103e\u1010\u103a\u1015\u102f\u1036\u1010\u1004\u103a\u1015\u102b\u104b",
        "registration_cancelled": "\u1019\u103e\u1010\u103a\u1015\u102f\u1036\u1010\u1004\u103a\u1001\u103c\u1004\u103a\u1038 \u1015\u101a\u103a\u1016\u103b\u1000\u103a\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b",
        "delete_account_done": "\u101e\u1004\u1037\u103a\u1021\u1000\u1031\u102c\u1004\u1037\u103a\u1000\u102d\u102f \u1016\u103b\u1000\u103a\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b \u101e\u1004\u1037\u103a\u1013\u102c\u1010\u103a\u1015\u102f\u1036\u1019\u103b\u102c\u1038\u1014\u1032\u1037 \u1016\u1030\u1038\u1005\u102c\u1006\u102f\u1036\u1001\u103b\u1000\u103a \u1021\u1001\u103b\u1000\u103a\u1021\u101c\u1000\u103a\u1021\u102c\u1038\u101c\u102f\u1036\u1038 \u1016\u103b\u1000\u103a\u101e\u103d\u102c\u1038\u1015\u102b\u1015\u103c\u102e\u104b",
        "banned": "\u101e\u1004\u1037\u103a\u1021\u1000\u1031\u102c\u1004\u1037\u103a\u1000\u102d\u102f \u1015\u102d\u1010\u103a\u1011\u102c\u1038\u1015\u102b\u1010\u101a\u103a\u104b",
        "no_profiles": "\u101a\u1001\u102f\u1021\u1001\u103b\u102d\u1014\u103a\u1010\u103d\u1004\u103a profile \u1019\u101b\u103e\u102d\u101e\u1031\u1038\u1015\u102b\u104b",
        "match": "\u1002\u102f\u100f\u103a\u101a\u1030\u1015\u102b\u1010\u101a\u103a\u104b \u101e\u1004\u103a\u1014\u1032\u1037 {name} \u1010\u102d\u102f\u1037 \u1016\u1030\u1038\u1005\u102c\u1006\u102f\u1036\u101e\u103d\u102c\u1038\u1015\u103c\u102e\u104b \U0001F60D",
        "match_username": "\u1002\u102f\u100f\u103a\u101a\u1030\u1015\u102b\u1010\u101a\u103a\u104b \u101e\u1004\u103a\u1014\u1032\u1037 {username} \u1010\u102d\u102f\u1037 \u1016\u1030\u1038\u1005\u102c\u1006\u102f\u1036\u101e\u103d\u102c\u1038\u1015\u103c\u102e\u104b \U0001F60D",
        "match_no_username": "\u1016\u1030\u1038\u1005\u102c\u1006\u102f\u1036\u101e\u103d\u102c\u1038\u1015\u103c\u102e\u104a \u1012\u102b\u1015\u1031\u1019\u101a\u1037\u103a \u1010\u1005\u103a\u1016\u1000\u103a\u101e\u1030\u1019\u103e\u102c Telegram username \u1019\u101e\u1010\u103a\u1019\u103e\u1010\u103a\u101b\u101e\u1031\u1038\u1015\u102b\u104b",
        "set_username_hint": "\u1016\u1030\u1038\u1005\u102c\u1006\u102f\u1036\u101e\u1030\u1010\u103d\u1031 \u101e\u1004\u1037\u103a\u1000\u102d\u102f \u101b\u103e\u102c\u1010\u103d\u1031\u1037\u1014\u102d\u102f\u1004\u103a\u101b\u1014\u103a Telegram Settings \u1019\u103e\u102c username \u101e\u1010\u103a\u1019\u103e\u1010\u103a\u1015\u1031\u1038\u1015\u102b\u104b",
        "like_received": "\u1010\u1005\u103a\u1016\u1000\u103a\u101e\u1030\u1000 \u101e\u1004\u1037\u103a\u1015\u101b\u102d\u102f\u1016\u102d\u102f\u1004\u103a\u1000\u102d\u102f \u1000\u103c\u102d\u102f\u1000\u103a\u1011\u102c\u1038\u1015\u102b\u1010\u101a\u103a\u104b \u1021\u1031\u102c\u1000\u103a\u1000\u1001\u101c\u102f\u1010\u103a\u1014\u1032\u1037 \u1015\u103c\u1014\u103a\u1000\u103c\u102d\u102f\u1000\u103a\u1014\u102d\u102f\u1004\u103a\u1015\u102b\u1010\u101a\u103a\u104b",
        "superlike_received": "{name} \u1000 \u101e\u1004\u1037\u103a\u1000\u102d\u102f SuperLike \u1015\u102d\u102f\u1037\u1011\u102c\u1038\u1015\u102b\u1010\u101a\u103a \U0001F31F",
        "already_premium": "\u101e\u1004\u103a Premium \u1021\u1010\u1000\u103a\u1010\u102d\u1015\u103a \u1016\u103c\u1005\u103a\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b",
        "premium_disabled": "\u1015\u101b\u102e\u1019\u102e\u101a\u1036 feature \u1019\u103b\u102c\u1038\u1000\u102d\u102f \u101a\u1001\u102f\u1021\u1001\u103b\u102d\u1014\u103a\u1010\u103d\u1004\u103a \u1015\u102d\u1010\u103a\u1011\u102c\u1038\u1015\u102b\u101e\u100a\u103a\u104b",
        "premium_intro": "\u1015\u101b\u102e\u1019\u102e\u101a\u1036\u1016\u103c\u1004\u1037\u103a Unlimited Likes\u104a \u101e\u1004\u1037\u103a\u1000\u102d\u102f \u1000\u103c\u102d\u102f\u1000\u103a\u1011\u102c\u1038\u101e\u1030\u1019\u103b\u102c\u1038\u104a Rewind \u1014\u103e\u1004\u1037\u103a Boost \u1021\u101e\u102f\u1036\u1038\u1015\u103c\u102f\u1014\u102d\u102f\u1004\u103a\u1015\u102b\u101e\u100a\u103a\u104b",
        "premium_buy_title": "\u1015\u101b\u102e\u1019\u102e\u101a\u1036 \u101d\u101a\u103a\u101a\u1030\u101b\u1014\u103a",
        "premium_choose_plan": "\u1015\u101b\u102e\u1019\u102e\u101a\u1036 plan \u101b\u103d\u1031\u1038\u1015\u102b\u104b",
        "premium_choose_provider": "\u1004\u103d\u1031\u1015\u1031\u1038\u1001\u103b\u1031\u1005\u1014\u1005\u103a \u101b\u103d\u1031\u1038\u1015\u102b\u104b",
        "premium_plan_weekly": "\u1010\u1005\u103a\u1015\u1010\u103a (1,500 MMK)",
        "premium_plan_monthly": "\u1010\u1005\u103a\u101c (3,000 MMK)",
        "premium_plan_selected": "\u101b\u103d\u1031\u1038\u1011\u102c\u1038\u101e\u100a\u1037\u103a plan: {plan}",
        "premium_payment_details": "\u1004\u103d\u1031\u101c\u103d\u103e\u1032\u101b\u1014\u103a\u1016\u102f\u1014\u103a\u1038: {phone}\n\u1011\u102d\u102f\u1037\u1014\u1031\u102c\u1000\u103a screenshot \u1015\u102d\u102f\u1037\u1015\u102b\u104b",
        "premium_send_receipt": "\u1004\u103d\u1031\u101c\u103d\u103e\u1032\u1015\u103c\u1031\u1005\u102c \u1015\u102d\u102f\u1037\u1015\u1031\u1038\u1015\u102b",
        "premium_submitted": "Screenshot \u1015\u102d\u102f\u1037\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b Admin \u1005\u1005\u103a\u1006\u1031\u1038\u1015\u1031\u1038\u1015\u102b\u1019\u100a\u103a\u104b",
        "premium_approved": "\u101e\u1004\u1037\u103a Premium \u1021\u1010\u100a\u103a\u1015\u103c\u102f\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b",
        "premium_rejected": "\u101e\u1004\u1037\u103a Premium \u101c\u103b\u103e\u1031\u102c\u1000\u103a\u1011\u102c\u1038\u1019\u103e\u102f \u1019\u1021\u1010\u100a\u103a\u1015\u103c\u102f\u1014\u102d\u102f\u1004\u103a\u1015\u102b\u104b",
        "premium_welcome": "Phu Sar Premium \u1021\u1000\u1031\u102c\u1004\u1037\u103a \u1016\u103d\u1004\u1037\u103a\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b Unlimited Swipes \u1021\u101e\u102f\u1036\u1038\u1015\u103c\u102f\u1014\u102d\u102f\u1004\u103a\u1015\u102b\u1015\u103c\u102e\u104b",
        "liked_you_intro": "\u101e\u1004\u1037\u103a\u1000\u102d\u102f \u1000\u103c\u102d\u102f\u1000\u103a\u1011\u102c\u1038\u101e\u1030\u1019\u103b\u102c\u1038",
        "liked_you_empty": "\u101e\u1004\u1037\u103a\u1000\u102d\u102f \u1000\u103c\u102d\u102f\u1000\u103a\u1011\u102c\u1038\u101e\u1030 \u1019\u101b\u103e\u102d\u101e\u1031\u1038\u1015\u102b\u104b",
        "liked_you_locked": "\u101e\u1004\u1037\u103a\u1000\u102d\u102f \u1000\u103c\u102d\u102f\u1000\u103a\u1011\u102c\u1038\u101e\u1030\u1019\u103b\u102c\u1038 \u1000\u103c\u100a\u1037\u103a\u101b\u1014\u103a Premium \u101c\u102d\u102f\u1021\u1015\u103a\u1015\u102b\u101e\u100a\u103a\u104b",
        "likes_limit_reached": "\u1019\u1031\u1037\u1014\u1031\u1037 like 30 \u1000\u103c\u102d\u1019\u103a \u1015\u103c\u100a\u1037\u103a\u101e\u103d\u102c\u1038\u1015\u103c\u102e\u104b Unlimited \u1021\u1010\u103d\u1000\u103a Premium \u101d\u101a\u103a\u101a\u1030\u1015\u102b\u104b",
        "rewind_done": "\u1014\u1031\u102c\u1000\u103a\u1006\u102f\u1036\u1038 Pass \u1000\u102d\u102f \u1015\u103c\u1014\u103a\u1016\u103d\u1004\u1037\u103a\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b",
        "rewind_missing": "Rewind \u101c\u102f\u1015\u103a\u101b\u1014\u103a Pass \u1019\u101b\u103e\u102d\u101e\u1031\u1038\u1015\u102b\u104b",
        "boost_done": "Boost \u1015\u102d\u102f\u1037\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b \u101e\u1004\u1037\u103a profile \u1000\u102d\u102f \u1014\u102e\u1038\u1005\u1015\u103a\u101e\u1030 100 \u101a\u1031\u102c\u1000\u103a\u1011\u102d \u1010\u1004\u103a\u1015\u1031\u1038\u1019\u100a\u103a\u104b",
        "boost_locked": "Boost \u1021\u101e\u102f\u1036\u1038\u1015\u103c\u102f\u101b\u1014\u103a Premium \u101c\u102d\u102f\u1021\u1015\u103a\u1015\u102b\u101e\u100a\u103a\u104b",
        "report_prompt": "Report \u1019\u102d\u1010\u1039\u1010\u1030 \u101b\u103d\u1031\u1038\u1015\u102b\u104b",
        "report_submitted": "Report \u1015\u102d\u102f\u1037\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b",
        "admin_only": "Admin \u101e\u102c \u1021\u101e\u102f\u1036\u1038\u1015\u103c\u102f\u1014\u102d\u102f\u1004\u103a\u1015\u102b\u101e\u100a\u103a\u104b",
        "user_banned": "User \u1015\u102d\u1010\u103a\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b",
        "user_unbanned": "User \u1015\u103c\u1014\u103a\u1016\u103d\u1004\u1037\u103a\u1015\u103c\u102e\u1038\u1015\u102b\u1015\u103c\u102e\u104b",
        "admin_approve_usage": "အသုံးပြုနည်း: /approve <user_id> <days>",
        "admin_reject_usage": "အသုံးပြုနည်း: /reject <user_id>",
        "admin_premium_done": "Premium ကို {days} ရက် အတည်ပြုပြီးပါပြီ။",
        "admin_reject_done": "Premium လျှောက်ထားမှု ငြင်းပယ်ပြီးပါပြီ။",
        "premium_no_pending": "ဒီ user အတွက် pending premium request မရှိပါ။",
        "profile_title": "\u101e\u1004\u1037\u103a\u1015\u101b\u102d\u102f\u1016\u102d\u102f\u1004\u103a",
        "label_age": "\u1021\u101e\u1000\u103a",
        "label_gender": "\u101c\u102d\u1004\u103a",
        "label_seeking": "\u101b\u103e\u102c\u1016\u103d\u1031\u101c\u102d\u102f\u101e\u1030",
        "label_location": "\u1014\u1031\u101b\u102c",
        "distance_away": "\U0001F4CD {km} \u1000\u102e\u101c\u102d\u102f\u1019\u102e\u1010\u102c \u1021\u1000\u103d\u102c",
        "btn_discover": "\u101b\u103e\u102c\u1016\u103d\u1031",
        "btn_premium": "\u1015\u101b\u102e\u1019\u102e\u101a\u1036 \u101d\u101a\u103a\u101a\u1030\u101b\u1014\u103a",
        "btn_profile": "\u1015\u101b\u102d\u102f\u1016\u102d\u102f\u1004\u103a",
        "btn_edit": "\u1015\u103c\u1004\u103a\u1006\u1004\u103a",
        "btn_liked_you": "\u101e\u1004\u1037\u103a\u1000\u102d\u102f \u1000\u103c\u102d\u102f\u1000\u103a\u1011\u102c\u1038\u101e\u1030\u1019\u103b\u102c\u1038",
        "btn_boost": "Boost",
        "btn_male": "\u1000\u103b\u102c\u1038",
        "btn_female": "\u1019",
        "btn_both": "\u1014\u103e\u1005\u103a\u1019\u103b\u102d\u102f\u1038\u101c\u102f\u1036\u1038",
        "btn_share_location": "\U0001F4CD \u1010\u100a\u103a\u1014\u1031\u101b\u102c \u1019\u103b\u103e\u101d\u1031\u1019\u100a\u103a",
        "btn_township_manual": "\U0001F3D9 \u1019\u103c\u102d\u102f\u1037\u1014\u101a\u103a\u1000\u102d\u102f \u1000\u102d\u102f\u101a\u103a\u1010\u102d\u102f\u1004\u103a \u101b\u103d\u1031\u1038\u1019\u100a\u103a",
        "btn_like": "\u2764\ufe0f",
        "btn_like_back": "\u2764\ufe0f \u1015\u103c\u1014\u103a\u1000\u103c\u102d\u102f\u1000\u103a\u1019\u101a\u103a",
        "btn_pass": "\u274C",
        "btn_superlike": "\U0001F31F Super",
        "btn_rewind": "\U0001F519 Rewind",
        "btn_report": "\U0001F6A9 \u1010\u102d\u102f\u1004\u103a\u1000\u103c\u102c\u1038",
        "btn_kbz": "KBZPay",
        "btn_wave": "WaveMoney",
        "btn_cancel": "\u1015\u101a\u103a\u1016\u103b\u1000\u103a",
    },
}


def t(lang: str, key: str, **kwargs: object) -> str:
    language = lang if lang in MESSAGES else "en"
    template = MESSAGES[language].get(key) or MESSAGES["en"].get(key) or key
    return template.format(**kwargs)


def region_label(lang: str, code: str) -> str:
    return REGION_LABELS.get(code, REGION_LABELS["other"]).get(lang, REGION_LABELS["other"]["en"])


def report_reason_label(lang: str, reason_code: str) -> str:
    return REPORT_REASON_LABELS.get(reason_code, REPORT_REASON_LABELS["spam"]).get(
        lang, REPORT_REASON_LABELS["spam"]["en"]
    )


def gender_label(lang: str, gender: str) -> str:
    if gender == "male":
        return t(lang, "btn_male")
    if gender == "female":
        return t(lang, "btn_female")
    return gender


def seeking_label(lang: str, value: str) -> str:
    if value == "male":
        return t(lang, "btn_male")
    if value == "female":
        return t(lang, "btn_female")
    if value == "both":
        return t(lang, "btn_both")
    return value
