from __future__ import annotations

from typing import Final


REGION_LABELS: Final[dict[str, dict[str, str]]] = {
    "yangon": {"en": "Yangon", "my": "ရန်ကုန်"},
    "mandalay": {"en": "Mandalay", "my": "မန္တလေး"},
    "naypyidaw": {"en": "Naypyidaw", "my": "နေပြည်တော်"},
    "bago": {"en": "Bago", "my": "ပဲခူး"},
    "ayeyarwady": {"en": "Ayeyarwady", "my": "ဧရာဝတီ"},
    "other": {"en": "Other", "my": "အခြား"},
}

REPORT_REASON_LABELS: Final[dict[str, dict[str, str]]] = {
    "fake": {"en": "Fake account", "my": "အကောင့်အတု"},
    "spam": {"en": "Spam", "my": "စပမ်း"},
    "inappropriate": {"en": "Inappropriate content", "my": "မသင့်လျော်သောအကြောင်းအရာ"},
    "abusive": {"en": "Abusive behavior", "my": "အပြုအမူမကောင်း"},
}

MESSAGES: Final[dict[str, dict[str, str]]] = {
    "en": {
        "lang_name": "English",
        "welcome": "Welcome to Phu Sar (ဖူးစာ). Start your journey to find your match.",
        "menu_text": "Choose an action:",
        "choose_language": "Choose your language:",
        "ask_gender": "Select your gender:",
        "ask_seeking": "Who are you looking for?",
        "ask_region": "Pick your region:",
        "ask_township": "Enter your township:",
        "ask_age": "Enter your age (18-99):",
        "ask_bio": "Write a short bio (max 500 chars):",
        "ask_photo": "Upload one clear profile photo:",
        "invalid_age": "Age must be a number between 18 and 99.",
        "invalid_text": "Please send text.",
        "invalid_photo": "Please upload a photo image.",
        "profile_saved": "Your profile is ready.",
        "profile_incomplete": "Complete registration first with /start.",
        "registration_cancelled": "Registration canceled.",
        "banned": "Your account is currently banned. Contact support.",
        "no_profiles": "No more profiles for now. Please try again later.",
        "match": "You matched with {name}. \U0001F60D",
        "already_premium": "You are already a premium user.",
        "premium_intro": "Premium unlocks better visibility and faster matching.",
        "premium_choose_provider": "Choose payment provider:",
        "premium_send_receipt": "Upload your KBZPay/WaveMoney payment screenshot.",
        "premium_submitted": "Payment screenshot submitted. Admin review is pending.",
        "premium_approved": "Your premium status is approved.",
        "premium_rejected": "Your premium request was rejected. Please submit a clearer receipt.",
        "report_prompt": "Select a reason to report this profile:",
        "report_submitted": "Thanks. Your report was submitted for moderation.",
        "admin_only": "This action is admin-only.",
        "user_banned": "User has been banned.",
        "user_unbanned": "User has been unbanned.",
        "profile_title": "Your profile",
        "label_age": "Age",
        "label_gender": "Gender",
        "label_seeking": "Seeking",
        "label_location": "Location",
        "btn_discover": "Discover",
        "btn_premium": "Premium",
        "btn_profile": "My Profile",
        "btn_edit": "Edit Profile",
        "btn_male": "Male",
        "btn_female": "Female",
        "btn_both": "Both",
        "btn_like": "\u2764\ufe0f Like",
        "btn_pass": "\u274C Pass",
        "btn_superlike": "\U0001F31F SuperLike",
        "btn_report": "\U0001F6A9 Report",
        "btn_kbz": "KBZPay",
        "btn_wave": "WaveMoney",
        "btn_cancel": "Cancel",
        "btn_approve": "Approve",
        "btn_reject": "Reject",
        "btn_ban": "Ban User",
        "btn_dismiss": "Dismiss",
    },
    "my": {
        "lang_name": "မြန်မာ",
        "welcome": "ဖူးစာ (Phu Sar) မှ ကြိုဆိုပါသည်။ သင့်ဖူးစာရှင်ကို ရှာဖွေဖို့ အောက်ကခလုတ်ကို နှိပ်ပါ။",
        "menu_text": "လုပ်ဆောင်ရန်တစ်ခုရွေးပါ။",
        "choose_language": "ဘာသာစကားရွေးပါ။",
        "ask_gender": "သင့်လိင်အမျိုးအစားရွေးပါ။",
        "ask_seeking": "ဘယ်သူကို ရှာချင်ပါသလဲ။",
        "ask_region": "နေထိုင်ရာတိုင်းဒေသကြီး/ပြည်နယ်ရွေးပါ။",
        "ask_township": "မြို့နယ်ကို ရိုက်ထည့်ပါ။",
        "ask_age": "အသက်ထည့်ပါ (18-99)။",
        "ask_bio": "ကိုယ်ရေးအကျဉ်းတို ရေးပါ (အများဆုံး 500 စာလုံး)။",
        "ask_photo": "Profile ဓာတ်ပုံတစ်ပုံတင်ပါ။",
        "invalid_age": "အသက်ကို 18 မှ 99 အတွင်း ကိန်းဂဏန်းဖြင့် ထည့်ပါ။",
        "invalid_text": "စာသားဖြင့် ဖြေပါ။",
        "invalid_photo": "ဓာတ်ပုံဖိုင်တင်ပေးပါ။",
        "profile_saved": "သင့်ပရိုဖိုင် သိမ်းဆည်းပြီးပါပြီ။",
        "profile_incomplete": "ပထမဦးစွာ /start နဲ့ မှတ်ပုံတင်ပါ။",
        "registration_cancelled": "မှတ်ပုံတင်ခြင်း ပယ်ဖျက်ပြီးပါပြီ။",
        "banned": "သင့်အကောင့်ကို ပိတ်ထားပါတယ်။ support ကို ဆက်သွယ်ပါ။",
        "no_profiles": "ယခုအချိန်တွင် ကြည့်ရန် profile မရှိသေးပါ။ နောက်မှ ပြန်စမ်းပါ။",
        "match": "ဂုဏ်ယူပါတယ်! သင်နဲ့ {name} တို့ ဖူးစာဆုံသွားပါပြီ။ \U0001F60D",
        "already_premium": "သင် Premium အသုံးပြုသူဖြစ်ပြီးပါပြီ။",
        "premium_intro": "Premium ဖြင့် မြင်သာမှု ပိုကောင်းပြီး match မြန်တက်နိုင်သည်။",
        "premium_choose_provider": "ငွေပေးချေမှုစနစ်ရွေးပါ။",
        "premium_send_receipt": "KBZPay/WaveMoney စာရင်းပေးချေ screenshot ကို တင်ပါ။",
        "premium_submitted": "Screenshot တင်ပြီးပါပြီ။ Admin စစ်ဆေးပြီး အတည်ပြုပေးပါမည်။",
        "premium_approved": "သင့် Premium အတည်ပြုပြီးပါပြီ။",
        "premium_rejected": "Premium လျှောက်ထားမှု မအတည်ပြုနိုင်ပါ။ screenshot ပိုရှင်းလင်းစွာ ပြန်တင်ပါ။",
        "report_prompt": "Report လုပ်ရမည့် အကြောင်းပြချက်ရွေးပါ။",
        "report_submitted": "ကျေးဇူးတင်ပါတယ်။ Report ကို moderation အဖွဲ့ထံ ပို့ပြီးပါပြီ။",
        "admin_only": "ဤလုပ်ဆောင်ချက်သည် Admin များအတွက်သာ ဖြစ်သည်။",
        "user_banned": "အသုံးပြုသူကို ပိတ်လိုက်ပါပြီ။",
        "user_unbanned": "အသုံးပြုသူကို ပြန်ဖွင့်လိုက်ပါပြီ။",
        "profile_title": "သင့်ပရိုဖိုင်",
        "label_age": "အသက်",
        "label_gender": "လိင်",
        "label_seeking": "ရှာဖွေလိုသူ",
        "label_location": "နေရာ",
        "btn_discover": "ရှာဖွေမည်",
        "btn_premium": "Premium",
        "btn_profile": "ပရိုဖိုင်",
        "btn_edit": "ပြင်ဆင်မည်",
        "btn_male": "ကျား",
        "btn_female": "မ",
        "btn_both": "နှစ်မျိုးလုံး",
        "btn_like": "\u2764\ufe0f ကြိုက်တယ်",
        "btn_pass": "\u274C ကျော်မယ်",
        "btn_superlike": "\U0001F31F အထူးကြိုက်",
        "btn_report": "\U0001F6A9 တိုင်ကြားမည်",
        "btn_kbz": "KBZPay",
        "btn_wave": "WaveMoney",
        "btn_cancel": "ပယ်ဖျက်မည်",
        "btn_approve": "အတည်ပြု",
        "btn_reject": "ငြင်းပယ်",
        "btn_ban": "User ပိတ်မည်",
        "btn_dismiss": "ပယ်ဖျက်",
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
