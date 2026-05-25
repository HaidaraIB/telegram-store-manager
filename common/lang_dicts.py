import models

TEXTS = {
    models.Language.ARABIC: {
        "user_welcome_msg": "أهلاً {name}",
        "admin_welcome_msg": "أهلاً بك...",
        "force_join_msg": (
            f"لبدء استخدام البوت يجب عليك الانضمام الى محادثة البوت أولاً\n\n"
            "<b>اشترك أولاً 👇</b>\n"
            "ثم اضغط <b>تحقق ✅</b>"
        ),
        "force_join_multiple_msg": (
            f"لبدء استخدام البوت يجب عليك الانضمام الى محادثات البوت أولاً\n\n"
            "<b>اشترك في جميع المحادثات 👇</b>\n"
            "ثم اضغط <b>تحقق ✅</b>"
        ),
        "join_first_answer": "قم بالاشتراك بالمحادثة أولاً ❗️",
        "join_all_first_answer": "قم بالاشتراك في جميع المحادثات أولاً ❗️",
        "settings": "الإعدادات ⚙️",
        "change_lang": "اختر اللغة 🌐",
        "change_lang_success": "تم تغيير اللغة بنجاح ✅",
        "home_page": "القائمة الرئيسية 🔝",
        "currently_admin": "تعمل الآن كآدمن 🕹",
        "admin_settings_title": "إعدادات الآدمن 🪄",
        "add_admin_instruction": (
            "اختر حساب الآدمن الذي تريد إضافته بالضغط على الزر أدناه\n\n"
            "يمكنك إرسال الid برسالة أيضاً\n\n"
            "أو إلغاء العملية بالضغط على /admin."
        ),
        "admin_added_success": "تمت إضافة الآدمن بنجاح ✅",
        "cannot_remove_owner": "لا يمكنك إزالة مالك البوت من قائمة الآدمنز ❗️",
        "admin_removed_success": "تمت إزالة الآدمن بنجاح ✅",
        "remove_admin_instruction": "اختر من القائمة أدناه الآدمن الذي تريد إزالته.",
        "continue_with_admin_command": "للمتابعة اضغط /admin",
        "keyboard_hidden": "تم الإخفاء ✅",
        "keyboard_shown": "تم الإظهار ✅",
        "ban_instruction": (
            "اختر حساب المستخدم الذي تريد حظره بالضغط على الزر أدناه\n\n"
            "يمكنك إرسال الid برسالة أيضاً\n\n"
            "أو إلغاء العملية بالضغط على /admin."
        ),
        "user_not_found": (
            "لم يتم العثور على المستخدم ❌\n"
            "تأكد من الآيدي أو من أن المستخدم قد بدأ محادثة مع البوت من قبل"
        ),
        "user_found": "تم العثور على المستخدم ✅",
        "do_you_want": "هل تريد",
        "operation_success": "تمت العملية بنجاح ✅",
        "ban_confirmation": (
            "معلومات المستخدم:\n"
            "{user_info}\n\n"
            "حالة الحظر الحالية: <b>{ban_status}</b>\n\n"
            "سيتم <b>{action}</b> هذا المستخدم.\n\n"
            "اضغط على زر <b>تأكيد</b> للمتابعة."
        ),
        "user_banned": "محظور 🔒",
        "user_not_banned": "غير محظور 🔓",
        "action_ban": "حظر",
        "action_unban": "فك حظر",
        "send_message": "أرسل الرسالة",
        "send_message_to": "هل تريد إرسال الرسالة إلى:",
        "send_user_ids": "قم بإرسال آيديات المستخدمين الذين تريد إرسال الرسالة لهم سطراً سطراً.",
        "send_chat_id": "أرسل آيدي القناة/المجموعة",
        "sending_messages": "يقوم البوت بإرسال الرسائل الآن، يمكنك متابعة استخدامه بشكل طبيعي",
        "bot_must_be_member": "يجب أن يكون البوت مشتركاً في هذه القناة/المجموعة حتى يتمكن من النشر فيها",
        "message_published_success": "تم نشر الرسالة في {chat_title} بنجاح ✅",
        "bot_owner": "مالك البوت",
        "force_join_chats_title": "إدارة محادثات الإجبار على الانضمام 💬",
        "add_force_join_chat_instruction": (
            "اختر المحادثة التي تريد إجبار المستخدمين على الانضمام إليها بالضغط على الزر أدناه\n\n"
            "يمكنك إرسال الid برسالة أيضاً\n\n"
            "أو إلغاء العملية بالضغط على /admin."
        ),
        "enter_chat_link_instruction": (
            "تم العثور على المحادثة: <b>{chat_title}</b>\n\n"
            "أرسل رابط المحادثة (invite link) أو اسم المستخدم\n\n"
            "مثال: https://t.me/channel_name أو @channel_name"
        ),
        "force_join_chat_added_success": "تمت إضافة محادثة الإجبار على الانضمام بنجاح ✅",
        "force_join_chat_removed_success": "تمت إزالة محادثة الإجبار على الانضمام بنجاح ✅",
        "remove_force_join_chat_instruction": "اختر من القائمة أدناه المحادثة التي تريد إزالتها.",
        "no_force_join_chats": "لا توجد محادثات إجبار على الانضمام حالياً ❗️",
        "force_join_chats_list_title": "قائمة محادثات الإجبار على الانضمام:",
        "invalid_chat_id": "آيدي المحادثة غير صحيح ❌",
        "chat_not_found": "لم يتم العثور على المحادثة ❌\nتأكد من الآيدي أو من أن البوت عضو في المحادثة",
        "chat_link_required": "المحادثة لا تحتوي على رابط دعوة. يرجى إرسال رابط الدعوة يدوياً.",
        "invalid_chat_link": "رابط المحادثة غير صحيح ❌\nيجب أن يبدأ بـ https://t.me/ أو @",
        "select_permissions_instruction": "اختر الصلاحيات التي تريد منحها لهذا الآدمن:",
        "permissions_selected": "تم اختيار الصلاحيات بنجاح ✅",
        "manage_permissions": "إدارة الصلاحيات 🔐",
        "edit_admin_permissions": "تعديل صلاحيات الآدمن 🔐",
        "select_admin_to_edit_permissions": "اختر الآدمن الذي تريد تعديل صلاحياته:",
        "current_permissions": "الصلاحيات الحالية:",
        "no_permissions": "لا توجد صلاحيات",
        "permission_granted": "تم منح الصلاحية ✅",
        "permission_revoked": "تم سحب الصلاحية ✅",
        "cannot_edit_owner_permissions": "لا يمكنك تعديل صلاحيات مالك البوت ❗️",
        "permission_ban_users": "حظر/فك حظر المستخدمين",
        "permission_broadcast": "إرسال رسائل جماعية",
        "permission_manage_force_join": "إدارة محادثات الإجبار على الانضمام",
        "permission_view_ids": "عرض معرفات المستخدمين/المحادثات",
        "permission_manage_permissions": "إدارة الصلاحيات",
        "permission_manage_admins": "إدارة الآدمنز",
        "permission_manage_users": "إدارة المستخدمين",
        "permission_manage_games": "إدارة الألعاب",
        "permission_manage_items": "إدارة العناصر",
        "permission_manage_payment_methods": "إدارة طرق الدفع",
        "permission_manage_general_settings": "إدارة الإعدادات العامة",
        "toggle_permission": "تبديل الصلاحية",
        "all_permissions": "جميع الصلاحيات",
        "no_permissions_selected": "لم يتم اختيار أي صلاحيات",
        "no_admins_to_edit": "لا يوجد أدمنز لتعديل صلاحياتهم",
        "you_dont_have_permission_to_manage_permissions": "لا يمكنك تعديل صلاحيات الآدمنز",
        "you_dont_have_permission_to_manage_admins": "لا يمكنك تعديل صلاحيات الآدمنز",
        "you_dont_have_permission_to_ban_users": "لا يمكنك تعديل صلاحيات الآدمنز",
        "you_dont_have_permission_to_broadcast": "لا يمكنك تعديل صلاحيات الآدمنز",
        "you_dont_have_permission_to_manage_force_join": "لا يمكنك تعديل صلاحيات الآدمنز",
        "you_dont_have_permission_to_view_ids": "لا يمكنك تعديل صلاحيات الآدمنز",
        "manage_users_settings_title": "إدارة المستخدمين 👥",
        "edit_user_balance": "تعديل رصيد المستخدم",
        "enter_user_id_for_balance": "أرسل معرف المستخدم الذي تريد تعديل رصيده:",
        "invalid_user_id": "معرف المستخدم غير صحيح ❌",
        "user_info": "معلومات المستخدم",
        "add_deduct_balance": "إضافة/خصم مبلغ",
        "set_new_balance": "تعيين رصيد جديد",
        "zero_balance": "تصفير الرصيد",
        "enter_amount_add_deduct": (
            "أرسل المبلغ الذي تريد إضافته أو خصمه:\n"
            "(للسالب أرسل رقم سالب، مثال: -50)"
        ),
        "enter_new_balance": "أرسل الرصيد الجديد:",
        "balance_zeroed": (
            "تم تصفير الرصيد بنجاح ✅\n"
            "الرصيد السابق: <code>{old_balance}</code> SDG"
        ),
        "balance_updated_add_deduct": (
            "تم {action} المبلغ بنجاح ✅\n"
            "الرصيد السابق: <code>{old_balance}</code> SDG\n"
            "المبلغ: <code>{amount}</code> SDG\n"
            "الرصيد الجديد: <code>{new_balance}</code> SDG"
        ),
        "balance_updated_set": (
            "تم تعيين الرصيد بنجاح ✅\n"
            "الرصيد السابق: <code>{old_balance}</code> SDG\n"
            "الرصيد الجديد: <code>{new_balance}</code> SDG"
        ),
        "export_users_to_excel": "تصدير المستخدمين إلى Excel 📊",
        "exporting_users": "جاري تصدير المستخدمين...",
        "users_exported_success": "تم تصدير المستخدمين بنجاح ✅",
        "export_error": "حدث خطأ أثناء التصدير ❌",
        "excel_user_id": "معرف المستخدم",
        "excel_username": "اسم المستخدم",
        "excel_name": "الاسم",
        "excel_language": "اللغة",
        "excel_is_admin": "آدمن",
        "excel_is_banned": "محظور",
        "excel_created_at": "تاريخ الإنشاء",
        "excel_no_username": "غير متوفر",
        "excel_unknown": "غير معروف",
        "excel_yes": "نعم",
        "excel_no": "لا",
        "lang_arabic": "العربية",
        "lang_english": "English",
        # Games Settings
        "games_settings_title": "إعدادات الألعاب 🎮",
        "add_game_instruction_name": "أرسل اسم اللعبة:",
        "add_game_instruction_code": "أرسل كود اللعبة (مثل: pubg, free_fire):",
        "game_code_exists": "الكود '{code}' موجود بالفعل. يرجى اختيار كود آخر.",
        "add_game_instruction_description": "أرسل وصف اللعبة (اختياري):",
        "game_added_success": "تمت إضافة اللعبة بنجاح ✅",
        "game_removed_success": "تمت إزالة اللعبة بنجاح ✅",
        "no_games": "لا توجد ألعاب حالياً ❗️",
        "remove_game_instruction": "اختر من القائمة أدناه اللعبة التي تريد إزالتها.",
        "games_list_title": "قائمة الألعاب:",
        "select_game_to_edit": "اختر اللعبة التي تريد تعديلها:",
        "edit_game_name": "تعديل اسم اللعبة",
        "edit_game_code": "تعديل كود اللعبة",
        "edit_game_description": "تعديل وصف اللعبة",
        "toggle_game_status": "تبديل حالة اللعبة",
        "enter_new_game_name": "أرسل الاسم الجديد للعبة:",
        "enter_new_game_code": "أرسل الكود الجديد للعبة:",
        "enter_new_game_description": "أرسل الوصف الجديد للعبة:",
        "game_name_updated": "تم تحديث اسم اللعبة بنجاح ✅",
        "game_code_updated": "تم تحديث كود اللعبة بنجاح ✅",
        "game_description_updated": "تم تحديث وصف اللعبة بنجاح ✅",
        "game_status_updated": "تم تحديث حالة اللعبة بنجاح ✅",
        # Items Settings
        "items_settings_title": "إعدادات العناصر 🎯",
        "no_active_games": "لا توجد ألعاب نشطة. يرجى إضافة لعبة أولاً.",
        "add_item_instruction_game": "اختر اللعبة التي ينتمي إليها العنصر:",
        "add_item_instruction_name": "أرسل اسم العنصر:",
        "add_item_instruction_type": "اختر نوع العنصر:",
        "add_item_instruction_price": "أرسل سعر العنصر:",
        "invalid_price": "السعر غير صحيح. يرجى إرسال رقم صحيح.",
        "add_item_instruction_description": "أرسل وصف العنصر (اختياري):",
        "add_item_instruction_stock": "أرسل كمية المخزون (اختياري، اتركه فارغاً إذا كان غير محدود):",
        "invalid_stock": "الكمية غير صحيحة. يرجى إرسال رقم صحيح.",
        "item_added_success": "تمت إضافة العنصر بنجاح ✅",
        "item_removed_success": "تمت إزالة العنصر بنجاح ✅",
        "no_items": "لا توجد عناصر حالياً ❗️",
        "select_game_to_remove_item": "اختر اللعبة لعرض عناصرها للحذف:",
        "remove_item_instruction": "اختر من القائمة أدناه العنصر الذي تريد إزالته:\nاللعبة: {game_name}",
        "items_list_title": "قائمة العناصر:",
        "select_game_to_edit_item": "اختر اللعبة لعرض عناصرها للتعديل:",
        "select_item_to_edit": "اختر العنصر الذي تريد تعديله:\nاللعبة: {game_name}",
        "no_items_for_game": "لا توجد عناصر لهذه اللعبة ❗️",
        "edit_item_name": "تعديل اسم العنصر",
        "edit_item_type": "تعديل نوع العنصر",
        "edit_item_price": "تعديل سعر العنصر",
        "edit_item_description": "تعديل وصف العنصر",
        "edit_item_stock": "تعديل كمية المخزون",
        "toggle_item_status": "تبديل حالة العنصر",
        "item_status_updated": "تم تحديث حالة العنصر بنجاح ✅",
        "enter_new_item_name": "أرسل الاسم الجديد للعنصر:",
        "select_new_item_type": "اختر النوع الجديد للعنصر:",
        "enter_new_item_price": "أرسل السعر الجديد للعنصر:",
        "enter_new_item_description": "أرسل الوصف الجديد للعنصر:",
        "enter_new_item_stock": "أرسل الكمية الجديدة للمخزون (اتركه فارغاً إذا كان غير محدود):",
        "invalid_item_type": "نوع العنصر غير صحيح ❌",
        "item_type_updated": "تم تحديث نوع العنصر بنجاح ✅",
        "item_name_updated": "تم تحديث اسم العنصر بنجاح ✅",
        "item_price_updated": "تم تحديث سعر العنصر بنجاح ✅",
        "item_description_updated": "تم تحديث وصف العنصر بنجاح ✅",
        "item_stock_updated": "تم تحديث كمية المخزون بنجاح ✅",
        # Payment Methods Settings
        "payment_methods_settings_title": "إعدادات طرق الدفع 💳",
        "add_payment_method_instruction_name": "أرسل اسم طريقة الدفع:",
        "add_payment_method_instruction_type": "اختر نوع طريقة الدفع:",
        "invalid_payment_type": "نوع طريقة الدفع غير صحيح ❌",
        "add_payment_method_instruction_description": "أرسل وصف طريقة الدفع (اختياري):",
        "payment_method_added_success": "تمت إضافة طريقة الدفع بنجاح ✅",
        "payment_method_removed_success": "تمت إزالة طريقة الدفع بنجاح ✅",
        "no_payment_methods": "لا توجد طرق دفع حالياً ❗️",
        "remove_payment_method_instruction": "اختر من القائمة أدناه طريقة الدفع التي تريد إزالتها.",
        "payment_methods_list_title": "قائمة طرق الدفع:",
        "select_payment_method_to_edit": "اختر طريقة الدفع التي تريد تعديلها:",
        "edit_payment_method_name": "تعديل اسم طريقة الدفع",
        "edit_payment_method_type": "تعديل نوع طريقة الدفع",
        "edit_payment_method_description": "تعديل وصف طريقة الدفع",
        "toggle_payment_method_status": "تبديل حالة طريقة الدفع",
        "payment_method_status_updated": "تم تحديث حالة طريقة الدفع بنجاح ✅",
        "enter_new_payment_method_name": "أرسل الاسم الجديد لطريقة الدفع:",
        "select_new_payment_method_type": "اختر النوع الجديد لطريقة الدفع:",
        "enter_new_payment_method_description": "أرسل الوصف الجديد لطريقة الدفع:",
        "payment_method_type_updated": "تم تحديث نوع طريقة الدفع بنجاح ✅",
        "payment_method_name_updated": "تم تحديث اسم طريقة الدفع بنجاح ✅",
        "payment_method_description_updated": "تم تحديث وصف طريقة الدفع بنجاح ✅",
        "select_payment_method_for_addresses": "اختر طريقة الدفع لإدارة عناوينها:",
        "payment_addresses_management": "إدارة عناوين الدفع",
        "select_payment_method_to_remove_address": "اختر طريقة الدفع لإزالة عنوان منها:",
        "remove_payment_address_instruction": "اختر العنوان الذي تريد إزالته:\nطريقة الدفع: {pm_name}",
        "no_payment_addresses": "لا توجد عناوين لهذه طريقة الدفع ❗️",
        "payment_method_paused": "طريقة الدفع {pm_name} متوقفة حالياً ⏸️",
        "payment_address_removed_success": "تمت إزالة عنوان الدفع بنجاح ✅",
        "add_payment_address_instruction_label": "أرسل تسمية العنوان (اختياري، اتركه فارغاً للمتابعة):",
        "add_payment_address_instruction_address": "أرسل عنوان الدفع (مطلوب):",
        "add_payment_address_instruction_account_name": "أرسل اسم الحساب (اختياري، اتركه فارغاً للمتابعة):",
        "add_payment_address_instruction_bank_name": "أرسل اسم البنك (اختياري، اتركه فارغاً للمتابعة):",
        "add_payment_address_instruction_branch": "أرسل اسم الفرع (اختياري، اتركه فارغاً للمتابعة):",
        "add_payment_address_instruction_additional_info": "أرسل معلومات إضافية (اختياري، اتركه فارغاً للمتابعة):",
        "payment_address_added_success": "تمت إضافة عنوان الدفع بنجاح ✅",
        # Common fields
        "active": "نشط ✅",
        "inactive": "غير نشط ❌",
        "status": "الحالة",
        "description": "الوصف",
        "type": "النوع",
        "price": "السعر",
        "game": "اللعبة",
        "stock": "المخزون",
        "select_what_to_edit": "اختر ما تريد تعديله:",
        "addresses_count": "عدد العناوين",
        "addresses": "العناوين",
        "created": "تاريخ الإنشاء",
        "updated": "تاريخ التحديث",
        "priority": "الأولوية",
        "address": "العنوان",
        "account_name": "اسم الحساب",
        "bank_name": "اسم البنك",
        "branch": "الفرع",
        "additional_info": "معلومات إضافية",
        "unlimited": "غير محدود",
        # Profile and Orders
        "profile_title": "الملف الشخصي 👤",
        "balance": "الرصيد",
        "current_balance": "رصيدك الحالي: <code>{balance}</code> SDG",
        "select_payment_method": "اختر طريقة الدفع:",
        "select_payment_address": "اختر عنوان الدفع:",
        "enter_charge_amount": "أدخل المبلغ الذي تريد شحنه:",
        "invalid_amount": "المبلغ غير صحيح ❌\nيجب أن يكون رقماً موجباً",
        "upload_payment_proof": "ارفع إثبات الدفع (صورة أو ملف):",
        "skip_payment_proof": "تخطي إثبات الدفع",
        "charge_balance_instructions": "أرسل المبلغ إلى أحد العناوين التالية وعند الانتهاء قم برفع إثبات الدفع:",
        "charge_balance_instructions_bank": "أرسل المبلغ إلى أحد الحسابات البنكية التالية وعند الانتهاء قم برفع إثبات الدفع (صورة من الإيصال أو كشف الحساب):",
        "charge_balance_instructions_e_wallet": "أرسل المبلغ إلى أحد محافظ الدفع الإلكتروني التالية وعند الانتهاء قم برفع إثبات الدفع (صورة من المعاملة):",
        "charge_balance_instructions_crypto": "أرسل المبلغ إلى أحد عناوين العملات المشفرة التالية وعند الانتهاء قم برفع إثبات الدفع (صورة من المعاملة):",
        "charge_balance_instructions_mobile_money": "أرسل المبلغ إلى أحد أرقام المحافظ النقدية التالية وعند الانتهاء قم برفع إثبات الدفع (صورة من المعاملة):",
        "charge_balance_instructions_other": "أرسل المبلغ إلى أحد العناوين التالية وعند الانتهاء قم برفع إثبات الدفع:",
        "charge_order_submitted": "تم إرسال طلب شحن الرصيد بنجاح ✅\nرقم الطلب: <code>{order_id}</code>",
        "charging_order_details": (
            "تفاصيل الطلب:\n"
            "الحالة: {status}\n"
            "المبلغ: <code>{amount}</code> SDG\n"
            "طريقة الدفع: <b>{payment_method}</b>\n"
            "عنوان الدفع: <code>{payment_address}</code>\n"
            "الرصيد الحالي: <code>{balance}</code> SDG"
        ),
        "select_game": "اختر اللعبة:",
        "select_item": "اختر العنصر:",
        "enter_game_account_id": "أدخل معرف حساب اللعبة الخاص بك:",
        "purchase_order_submitted": "تم إرسال طلب الشراء بنجاح ✅\nرقم الطلب: <code>{order_id}</code>",
        "select_order_type": "اختر نوع الطلبات:",
        "no_orders": "لا توجد طلبات ❗️",
        "charging_balance_orders": "طلبات شحن الرصيد",
        "purchase_orders": "طلبات الشراء",
        "api_purchase_orders": "طلبات الشراء الفورية ⚡",
        "order_details_text": "تفاصيل الطلب",
        "order_id": "رقم الطلب",
        "order_status": "حالة الطلب",
        "order_amount": "المبلغ",
        "order_date": "تاريخ الطلب",
        "payment_method": "طريقة الدفع",
        "payment_address": "عنوان الدفع",
        "payment_proof": "إثبات الدفع",
        "game_account_id": "معرف حساب اللعبة",
        "item_name": "اسم العنصر",
        "game_name": "اسم اللعبة",
        "order_status_pending": "قيد الانتظار",
        "order_status_processing": "قيد المعالجة",
        "order_status_completed": "مكتمل",
        "order_status_cancelled": "ملغي",
        "order_status_refunded": "مسترد",
        "order_status_failed": "فشل",
        "insufficient_balance": (
            "رصيدك غير كافٍ ❌\n"
            "رصيدك الحالي: {balance} SDG\n"
            "السعر المطلوب: {price} SDG"
        ),
        "insufficient_balance_charge": (
            "رصيدك غير كافٍ ❌\n"
            "رصيدك الحالي: {balance} SDG\n"
            "السعر المطلوب: {price} SDG\n\n"
            "يرجى شحن رصيدك أولاً 💰"
        ),
        "item_not_found": "العنصر غير موجود أو غير نشط ❌",
        "order_not_found": "الطلب غير موجود ❌",
        "admin_notes": "ملاحظات الآدمن",
        "select_order": "اختر طلباً لعرضه:",
        "orders_settings": "إدارة الطلبات 📋",
        "orders_settings_title": "إدارة الطلبات 📋",
        # General Settings
        "general_settings_title": "الإعدادات العامة ⚙️",
        "api_provider_settings_title": "اختر المزود النشط (واحد فقط):\n\nالحالي: {provider}",
        "api_provider_updated": "تم تحديث المزود ✅",
        "api_provider_switch_warning": "تم التحديث. راجع تصفية ألعاب API للكتالوج الجديد. الطلبات المعلقة تبقى على المزود الأصلي.",
        "api_provider": "المزود",
        "api_provider_g2bulk": "G2Bulk",
        "api_provider_gamevouchers": "Game Vouchers",
        "voucher_codes": "أكواد القسائم",
        "order_async_hint": "طلبك قيد المعالجة. سيتم إشعارك عند الاكتمال.",
        "current_usd_to_sudan_rate": "سعر الصرف الحالي: <code>{rate}</code>",
        "enter_usd_to_sudan_rate": (
            "أدخل سعر صرف الدولار إلى العملة السودانية:\n"
            "السعر الحالي: <code>{current_rate}</code>"
        ),
        "invalid_rate": "سعر الصرف غير صحيح ❌\nيجب أن يكون رقماً موجباً",
        "rate_updated_success": (
            "تم تحديث سعر الصرف بنجاح ✅\n" "السعر الجديد: <code>{rate}</code>"
        ),
        "change_status": "تغيير الحالة",
        "add_notes": "إضافة ملاحظات",
        "select_order_status": "اختر حالة الطلب:",
        "enter_order_notes": "أدخل الملاحظات لهذا الطلب:",
        "order_notes_added": "تمت إضافة الملاحظات بنجاح ✅",
        "reply_to_order_for_notes": "📝 قم بالرد على رسالة الطلب أعلاه لإضافة ملاحظات لهذا الطلب.",
        "reply_to_order_for_amount": "💰 قم بالرد على رسالة الطلب أعلاه مع المبلغ الجديد (رقم فقط).",
        "notes_empty": "الملاحظات لا يمكن أن تكون فارغة ❌",
        "order_not_found_in_reply": "تعذر تحديد الطلب من الرسالة المرد عليها. يرجى استخدام زر 'إضافة ملاحظات' على رسالة الطلب.",
        "order_amount_updated": "تم تحديث المبلغ بنجاح ✅\nالمبلغ القديم: {old_amount} SDG\nالمبلغ الجديد: {new_amount} SDG",
        "edit_amount": "تعديل المبلغ",
        "order_status_updated": "تم تحديث حالة الطلب بنجاح ✅",
        "order_already_assigned": "⚠️ هذا الطلب قيد المعالجة من قبل مشرف آخر",
        "order_status_terminal": "⚠️ لا يمكن تغيير حالة الطلب لأنه في حالة نهائية",
        "charging_order_status_changed": "🔔 <b>تم تحديث حالة طلب شحن الرصيد</b>\n\n",
        "purchase_order_status_changed": "🔔 <b>تم تحديث حالة طلب الشراء</b>\n\n",
        "user": "المستخدم",
        "user_id": "معرف المستخدم",
        "username": "اسم المستخدم",
        "name": "الاسم",
        "not_available": "غير متوفر",
        "no_pending_orders": "لا توجد طلبات قيد الانتظار أو قيد المعالجة ❗️",
        "select_game_api": "اختر اللعبة للشراء الفوري:",
        "search_game_hint": "\n\n💡 يمكنك أيضاً كتابة اسم اللعبة للبحث عنها",
        # Instant Purchase (API)
        "loading_game_catalog": "جاري تحميل قائمة الحزم...",
        "select_denomination": "اختر الحزمة:",
        "no_search_results": "❌ لم يتم العثور على نتائج للبحث",
        "search_results": "🔍 نتائج البحث:",
        "enter_player_id": "أدخل معرف اللاعب (Player ID):",
        "enter_server_id": "أدخل معرف السيرفر (Server ID):",
        "validating_player_id": "جاري التحقق من معرف اللاعب...",
        "player_id_valid": "تم التحقق من معرف اللاعب ✅\nالاسم: {player_name}",
        "player_id_invalid": "معرف اللاعب غير صحيح ❌",
        "server_not_required": "هذه اللعبة لا تحتاج إلى سيرفر",
        "confirm_order": "تأكيد الطلب",
        "order_processing": "جاري معالجة الطلب...",
        "order_created_success": "تم إنشاء الطلب بنجاح ✅\nرقم الطلب: {order_id}",
        "order_created_error": "حدث خطأ أثناء إنشاء الطلب ❌\n{error}",
        "insufficient_balance_api": (
            "رصيدك غير كافٍ ❌\n"
            "رصيدك الحالي: {balance} SDG\n"
            "السعر المطلوب: {price} SDG"
        ),
        "product_out_of_stock": ("هذا المنتج غير متوفر حالياً ❌\n" "نعتذر عن الإزعاج"),
        "no_games_available": "لا توجد ألعاب متاحة حالياً ❗️",
        "no_filtered_games_available": "لا توجد ألعاب متاحة. يرجى الاتصال بالمسؤول.",
        "game_not_available": "هذه اللعبة غير متاحة",
        "no_denominations_available": "لا توجد حزم متاحة لهذه اللعبة ❗️",
        # API Purchase Order Statuses
        "api_order_status_pending": "قيد الانتظار",
        "api_order_status_processing": "قيد المعالجة",
        "api_order_status_completed": "مكتمل",
        "api_order_status_failed": "فشل",
        "api_order_status_cancelled": "ملغي",
        "api_order_completed": "تم إكمال طلبك بنجاح!",
        "api_order_failed": "فشل طلبك.",
        "api_order_cancelled": "تم إلغاء طلبك.",
        "balance_refunded": "تم إرجاع رصيدك: {amount} SDG",
        "api_order_id": "رقم الطلب من API",
        "player_id": "رقم اللاعب",
        "player_name": "اسم اللاعب",
        "denomination": "الحزمة",
        "server_id": "معرف الخادم",
        "message": "رسالة",
        "remark": "ملاحظة",
        "api_error": "حدث خطأ في الاتصال بالخدمة ❌",
        "order_confirm_summary": (
            "<b>تأكيد الطلب</b>\n\n"
            "🎮 <b>اللعبة:</b> {game_name}\n"
            "📦 <b>الحزمة:</b> {denomination}\n"
            "{quantity_line}"
            "💰 <b>السعر:</b> <code>{price} SDG</code>\n"
            "{player_line}"
            "{server_line}\n"
            "💳 <b>رصيدك الحالي:</b> <code>{balance} SDG</code>\n\n"
            "اضغط <b>تأكيد</b> لإتمام الشراء، أو <b>إلغاء</b> للخروج دون خصم أي رصيد."
        ),
        "order_confirm_quantity_line": "🔢 <b>الكمية:</b> {quantity}\n",
        "enter_quantity": "أدخل الكمية (1-{max}):",
        "invalid_quantity": "كمية غير صالحة. أدخل رقماً من 1 إلى {max}.",
        "voucher_quantity_details_text": (
            "<b>تفاصيل المنتج:</b>\n\n"
            "🎮 <b>اللعبة:</b> {game_name}\n"
            "📦 <b>الحزمة:</b> {denomination}\n"
            "💰 <b>سعر الوحدة:</b> <code>{unit_price}</code> SDG\n\n"
            "{enter_quantity}"
        ),
        "api_purchase_cancelled_no_charge": "تم إلغاء الطلب. لم يتم خصم أي رصيد من حسابك ✅",
        "player_id_required": "معرف اللاعب مطلوب لهذا المنتج ❗️",
        "order_details_header": "تفاصيل الطلب:\n",
        "order_details": (
            "تفاصيل الطلب:\n"
            "اللعبة: <b>{game_name}</b>\n"
            "الحزمة: <b>{denomination}</b>\n"
            "السعر: <code>{price} SDG</code>\n"
            "معرف اللاعب: <code>{player_id}</code>\n"
            "الرصيد الحالي: <code>{balance}</code>"
        ),
        "manual_order_details": (
            "تفاصيل الطلب:\n"
            "الحالة: {status}\n"
            "المنتج: <b>{item_name}</b>\n"
            "اللعبة: <b>{game_name}</b>\n"
            "السعر: <code>{price}</code> SDG\n"
            "معرف الحساب: <code>{game_account_id}</code>\n"
            "الرصيد الحالي: <code>{balance}</code> SDG"
        ),
        "product_details": "تفاصيل المنتج 📦",
        "product_details_text": (
            "<b>تفاصيل المنتج:</b>\n\n"
            "🎮 <b>اللعبة:</b> {game_name}\n"
            "📦 <b>الحزمة:</b> {denomination}\n"
            "💰 <b>السعر:</b> <code>{price}</code> SDG\n\n"
            "{enter_player_id}"
        ),
        # Filter API Games
        "filter_api_games_settings_title": "إعدادات تصفية ألعاب API 🔍",
        "select_api_game_to_manage": "اختر لعبة للتحكم:",
        "api_games_list_info": "🟢 = اللعبة موجودة ونشطة\n🔴 = اللعبة غير موجودة أو غير نشطة",
        "enter_arabic_name": "أدخل الاسم العربي للعبة:",
        "arabic_name_saved": "تم حفظ الاسم العربي بنجاح ✅",
        "api_game_status_updated": "تم تحديث حالة اللعبة بنجاح ✅",
        "set_arabic_name": "تعيين الاسم العربي",
        "toggle_api_game_status": "تبديل الحالة",
        "original_name": "الاسم الأصلي",
        "arabic_name": "الاسم العربي",
        "select_filtered_game_to_manage": "اختر لعبة مصفاة للتحكم:",
        "filtered_games_list_info": "🟢 = نشط\n🔴 = غير نشط",
        "no_filtered_games": "لا توجد ألعاب مصفاة. يرجى تصفية الألعاب من API أولاً.",
        "game_not_found": "اللعبة غير موجودة",
        "order_user_info": "معلومات صاحب الطلب",
    },
    models.Language.ENGLISH: {
        "user_welcome_msg": "Welcome {name}",
        "admin_welcome_msg": "Welcome...",
        "force_join_msg": (
            f"You have to join the bot's chat in order to be able to use it\n\n"
            "<b>Join First 👇</b>\n"
            "And then press <b>Verify ✅</b>"
        ),
        "force_join_multiple_msg": (
            f"You have to join the bot's chats in order to be able to use it\n\n"
            "<b>Join all chats 👇</b>\n"
            "And then press <b>Verify ✅</b>"
        ),
        "join_first_answer": "Join the chat first ❗️",
        "join_all_first_answer": "Join all chats first ❗️",
        "settings": "Settings ⚙️",
        "change_lang": "Choose a language 🌐",
        "change_lang_success": "Language changed ✅",
        "home_page": "Home page 🔝",
        "currently_admin": "You're currently an Admin 🕹",
        "admin_settings_title": "Admin Settings 🪄",
        "add_admin_instruction": (
            "Choose the admin account you want to add by clicking the button below\n\n"
            "You can also send the ID in a message\n\n"
            "Or cancel the operation by pressing /admin."
        ),
        "admin_added_success": "Admin added successfully ✅",
        "cannot_remove_owner": "You cannot remove the bot owner from the admin list ❗️",
        "admin_removed_success": "Admin removed successfully ✅",
        "remove_admin_instruction": "Choose from the list below the admin you want to remove.",
        "continue_with_admin_command": "To continue press /admin",
        "keyboard_hidden": "Hidden ✅",
        "keyboard_shown": "Shown ✅",
        "ban_instruction": (
            "Choose the user account you want to ban by clicking the button below\n\n"
            "You can also send the ID in a message\n\n"
            "Or cancel the operation by pressing /admin."
        ),
        "user_not_found": (
            "User not found ❌\n"
            "Make sure of the ID or that the user has started a conversation with the bot before"
        ),
        "user_found": "User found ✅",
        "do_you_want": "Do you want to",
        "operation_success": "Operation completed successfully ✅",
        "ban_confirmation": (
            "User Information:\n"
            "{user_info}\n\n"
            "Current Ban Status: <b>{ban_status}</b>\n\n"
            "This user will be <b>{action}</b>.\n\n"
            "Press the <b>Confirm</b> button to proceed."
        ),
        "user_banned": "Banned 🔒",
        "user_not_banned": "Not Banned 🔓",
        "action_ban": "ban",
        "action_unban": "unban",
        "send_message": "Send the message",
        "send_message_to": "Who do you want to send the message to:",
        "send_user_ids": "Send the user IDs you want to send the message to, one per line.",
        "send_chat_id": "Send the channel/group ID",
        "sending_messages": "The bot is sending messages now, you can continue using it normally",
        "bot_must_be_member": "The bot must be a member of this channel/group to be able to post in it",
        "message_published_success": "Message published in {chat_title} successfully ✅",
        "bot_owner": "Bot Owner",
        "force_join_chats_title": "Manage Force Join Chats 💬",
        "add_force_join_chat_instruction": (
            "Choose the chat you want to force users to join by clicking the button below\n\n"
            "You can also send the ID in a message\n\n"
            "Or cancel the operation by pressing /admin."
        ),
        "enter_chat_link_instruction": (
            "Chat found: <b>{chat_title}</b>\n\n"
            "Send the chat invite link or username\n\n"
            "Example: https://t.me/channel_name or @channel_name"
        ),
        "force_join_chat_added_success": "Force join chat added successfully ✅",
        "force_join_chat_removed_success": "Force join chat removed successfully ✅",
        "remove_force_join_chat_instruction": "Choose from the list below the chat you want to remove.",
        "no_force_join_chats": "No force join chats currently ❗️",
        "force_join_chats_list_title": "Force Join Chats List:",
        "invalid_chat_id": "Invalid chat ID ❌",
        "chat_not_found": "Chat not found ❌\nMake sure of the ID or that the bot is a member of the chat",
        "chat_link_required": "The chat doesn't have an invite link. Please send the invite link manually.",
        "invalid_chat_link": "Invalid chat link ❌\nMust start with https://t.me/ or @",
        "select_permissions_instruction": "Select the permissions you want to grant to this admin:",
        "permissions_selected": "Permissions selected successfully ✅",
        "manage_permissions": "Manage Permissions 🔐",
        "edit_admin_permissions": "Edit Admin Permissions 🔐",
        "select_admin_to_edit_permissions": "Select the admin whose permissions you want to edit:",
        "current_permissions": "Current Permissions:",
        "no_permissions": "No permissions",
        "permission_granted": "Permission granted ✅",
        "permission_revoked": "Permission revoked ✅",
        "cannot_edit_owner_permissions": "You cannot edit the bot owner's permissions ❗️",
        "permission_ban_users": "Ban/Unban Users",
        "permission_broadcast": "Broadcast Messages",
        "permission_manage_force_join": "Manage Force Join Chats",
        "permission_view_ids": "View User/Chat IDs",
        "permission_manage_permissions": "Manage Permissions",
        "permission_manage_admins": "Manage Admins",
        "permission_manage_users": "Manage Users",
        "permission_manage_games": "Manage Games",
        "permission_manage_items": "Manage Items",
        "permission_manage_payment_methods": "Manage Payment Methods",
        "permission_manage_general_settings": "Manage General Settings",
        "toggle_permission": "Toggle Permission",
        "all_permissions": "All Permissions",
        "no_permissions_selected": "No permissions selected",
        "no_admins_to_edit": "No admins to edit permissions",
        "you_dont_have_permission_to_manage_permissions": "You don't have permission to manage permissions",
        "you_dont_have_permission_to_manage_admins": "You don't have permission to manage admins",
        "you_dont_have_permission_to_ban_users": "You don't have permission to ban users",
        "you_dont_have_permission_to_broadcast": "You don't have permission to broadcast",
        "you_dont_have_permission_to_manage_force_join": "You don't have permission to manage force join chats",
        "you_dont_have_permission_to_view_ids": "You don't have permission to view user/chat IDs",
        "manage_users_settings_title": "Manage Users 👥",
        "export_users_to_excel": "Export Users to Excel 📊",
        "edit_user_balance": "Edit User Balance",
        "enter_user_id_for_balance": "Send the user ID whose balance you want to edit:",
        "invalid_user_id": "Invalid user ID ❌",
        "user_info": "User Information",
        "add_deduct_balance": "Add/Deduct Amount",
        "set_new_balance": "Set New Balance",
        "zero_balance": "Zero Balance",
        "enter_amount_add_deduct": (
            "Send the amount you want to add or deduct:\n"
            "(For negative, send a negative number, e.g., -50)"
        ),
        "enter_new_balance": "Send the new balance:",
        "balance_zeroed": (
            "Balance zeroed successfully ✅\n"
            "Previous balance: <code>{old_balance}</code> SDG"
        ),
        "balance_updated_add_deduct": ("Amount {action} successfully ✅\n"
            "Previous balance: <code>{old_balance}</code> SDG\n"
            "Amount: <code>{amount}</code> SDG\n"
            "New balance: <code>{new_balance}</code> SDG"
        ),
        "balance_updated_set": (
            "Balance set successfully ✅\n"
            "Previous balance: <code>{old_balance}</code> SDG\n"
            "New balance: <code>{new_balance}</code> SDG"
        ),
        "exporting_users": "Exporting users...",
        "users_exported_success": "Users exported successfully ✅",
        "export_error": "An error occurred while exporting ❌",
        "excel_user_id": "User ID",
        "excel_username": "Username",
        "excel_name": "Name",
        "excel_language": "Language",
        "excel_is_admin": "Is Admin",
        "excel_is_banned": "Is Banned",
        "excel_created_at": "Created At",
        "excel_no_username": "N/A",
        "excel_unknown": "Unknown",
        "excel_yes": "Yes",
        "excel_no": "No",
        "lang_arabic": "Arabic",
        "lang_english": "English",
        # Games Settings
        "games_settings_title": "Games Settings 🎮",
        "add_game_instruction_name": "Send the game name:",
        "add_game_instruction_code": "Send the game code (e.g., pubg, free_fire):",
        "game_code_exists": "The code '{code}' already exists. Please choose another code.",
        "add_game_instruction_description": "Send the game description (optional):",
        "game_added_success": "Game added successfully ✅",
        "game_removed_success": "Game removed successfully ✅",
        "no_games": "No games currently ❗️",
        "remove_game_instruction": "Choose from the list below the game you want to remove.",
        "games_list_title": "Games List:",
        "select_game_to_edit": "Select the game you want to edit:",
        "edit_game_name": "Edit Game Name",
        "edit_game_code": "Edit Game Code",
        "edit_game_description": "Edit Game Description",
        "toggle_game_status": "Toggle Game Status",
        "enter_new_game_name": "Send the new game name:",
        "enter_new_game_code": "Send the new game code:",
        "enter_new_game_description": "Send the new game description:",
        "game_name_updated": "Game name updated successfully ✅",
        "game_code_updated": "Game code updated successfully ✅",
        "game_description_updated": "Game description updated successfully ✅",
        "game_status_updated": "Game status updated successfully ✅",
        # Items Settings
        "items_settings_title": "Items Settings 🎯",
        "no_active_games": "No active games. Please add a game first.",
        "add_item_instruction_game": "Select the game this item belongs to:",
        "add_item_instruction_name": "Send the item name:",
        "add_item_instruction_type": "Select the item type:",
        "add_item_instruction_price": "Send the item price:",
        "invalid_price": "Invalid price. Please send a valid number.",
        "add_item_instruction_description": "Send the item description (optional):",
        "add_item_instruction_stock": "Send the stock quantity (optional, leave empty if unlimited):",
        "invalid_stock": "Invalid quantity. Please send a valid number.",
        "item_added_success": "Item added successfully ✅",
        "item_removed_success": "Item removed successfully ✅",
        "no_items": "No items currently ❗️",
        "select_game_to_remove_item": "Select the game to show its items for removal:",
        "remove_item_instruction": "Choose from the list below the item you want to remove:\nGame: {game_name}",
        "items_list_title": "Items List:",
        "select_game_to_edit_item": "Select the game to show its items for editing:",
        "select_item_to_edit": "Select the item you want to edit:\nGame: {game_name}",
        "no_items_for_game": "No items for this game ❗️",
        "edit_item_name": "Edit Item Name",
        "edit_item_type": "Edit Item Type",
        "edit_item_price": "Edit Item Price",
        "edit_item_description": "Edit Item Description",
        "edit_item_stock": "Edit Stock Quantity",
        "toggle_item_status": "Toggle Item Status",
        "item_status_updated": "Item status updated successfully ✅",
        "enter_new_item_name": "Send the new item name:",
        "select_new_item_type": "Select the new item type:",
        "enter_new_item_price": "Send the new item price:",
        "enter_new_item_description": "Send the new item description:",
        "enter_new_item_stock": "Send the new stock quantity (leave empty if unlimited):",
        "invalid_item_type": "Invalid item type ❌",
        "item_type_updated": "Item type updated successfully ✅",
        "item_name_updated": "Item name updated successfully ✅",
        "item_price_updated": "Item price updated successfully ✅",
        "item_description_updated": "Item description updated successfully ✅",
        "item_stock_updated": "Item stock updated successfully ✅",
        # Payment Methods Settings
        "payment_methods_settings_title": "Payment Methods Settings 💳",
        "add_payment_method_instruction_name": "Send the payment method name:",
        "add_payment_method_instruction_type": "Select the payment method type:",
        "invalid_payment_type": "Invalid payment type ❌",
        "add_payment_method_instruction_description": "Send the payment method description (optional):",
        "payment_method_added_success": "Payment method added successfully ✅",
        "payment_method_removed_success": "Payment method removed successfully ✅",
        "no_payment_methods": "No payment methods currently ❗️",
        "remove_payment_method_instruction": "Choose from the list below the payment method you want to remove.",
        "payment_methods_list_title": "Payment Methods List:",
        "select_payment_method_to_edit": "Select the payment method you want to edit:",
        "edit_payment_method_name": "Edit Payment Method Name",
        "edit_payment_method_type": "Edit Payment Method Type",
        "edit_payment_method_description": "Edit Payment Method Description",
        "toggle_payment_method_status": "Toggle Payment Method Status",
        "payment_method_status_updated": "Payment method status updated successfully ✅",
        "enter_new_payment_method_name": "Send the new payment method name:",
        "select_new_payment_method_type": "Select the new payment method type:",
        "enter_new_payment_method_description": "Send the new payment method description:",
        "payment_method_type_updated": "Payment method type updated successfully ✅",
        "payment_method_name_updated": "Payment method name updated successfully ✅",
        "payment_method_description_updated": "Payment method description updated successfully ✅",
        "select_payment_method_for_addresses": "Select the payment method to manage its addresses:",
        "payment_addresses_management": "Payment Addresses Management",
        "select_payment_method_to_remove_address": "Select the payment method to remove an address from:",
        "remove_payment_address_instruction": "Select the address you want to remove:\nPayment Method: {pm_name}",
        "no_payment_addresses": "No addresses for this payment method ❗️",
        "payment_method_paused": "Payment method {pm_name} is currently paused ⏸️",
        "payment_address_removed_success": "Payment address removed successfully ✅",
        "add_payment_address_instruction_label": "Send the address label (optional, leave empty to continue):",
        "add_payment_address_instruction_address": "Send the payment address (required):",
        "add_payment_address_instruction_account_name": "Send the account name (optional, leave empty to continue):",
        "add_payment_address_instruction_bank_name": "Send the bank name (optional, leave empty to continue):",
        "add_payment_address_instruction_branch": "Send the branch name (optional, leave empty to continue):",
        "add_payment_address_instruction_additional_info": "Send additional information (optional, leave empty to continue):",
        "payment_address_added_success": "Payment address added successfully ✅",
        # Common fields
        "active": "Active ✅",
        "inactive": "Inactive ❌",
        "status": "Status",
        "description": "Description",
        "type": "Type",
        "price": "Price",
        "game": "Game",
        "stock": "Stock",
        "select_what_to_edit": "Select what you want to edit:",
        "addresses_count": "Addresses Count",
        "addresses": "Addresses",
        "created": "Created",
        "updated": "Updated",
        "priority": "Priority",
        "address": "Address",
        "account_name": "Account Name",
        "bank_name": "Bank Name",
        "branch": "Branch",
        "additional_info": "Additional Info",
        "unlimited": "Unlimited",
        # Profile and Orders
        "profile_title": "Profile 👤",
        "balance": "Balance",
        "current_balance": "Your current balance: <code>{balance}</code>",
        "select_payment_method": "Select payment method:",
        "select_payment_address": "Select payment address:",
        "enter_charge_amount": "Enter the amount you want to charge:",
        "invalid_amount": "Invalid amount ❌\nMust be a positive number",
        "upload_payment_proof": "Upload payment proof (image or file):",
        "skip_payment_proof": "Skip payment proof",
        "charge_balance_instructions": "Send the money to one of the following addresses and when you're finished provide a payment proof:",
        "charge_balance_instructions_bank": "Send the money to one of the following bank accounts and when you're finished provide a payment proof (receipt or bank statement):",
        "charge_balance_instructions_e_wallet": "Send the money to one of the following e-wallets and when you're finished provide a payment proof (transaction screenshot):",
        "charge_balance_instructions_crypto": "Send the money to one of the following cryptocurrency addresses and when you're finished provide a payment proof (transaction screenshot):",
        "charge_balance_instructions_mobile_money": "Send the money to one of the following mobile money numbers and when you're finished provide a payment proof (transaction screenshot):",
        "charge_balance_instructions_other": "Send the money to one of the following addresses and when you're finished provide a payment proof:",
        "charge_order_submitted": "Charging balance order submitted successfully ✅\nOrder ID: <code>{order_id}</code>",
        "charging_order_details": (
            "Order Details:\n"
            "Status: {status}\n"
            "Amount: <code>{amount}</code> SDG\n"
            "Payment Method: <b>{payment_method}</b>\n"
            "Payment Address: <code>{payment_address}</code>\n"
            "Current Balance: <code>{balance}</code> SDG"
        ),
        "select_game": "Select game:",
        "select_item": "Select item:",
        "enter_game_account_id": "Enter your game account ID:",
        "purchase_order_submitted": "Purchase order submitted successfully ✅\nOrder ID: <code>{order_id}</code>",
        "select_order_type": "Select order type:",
        "no_orders": "No orders ❗️",
        "charging_balance_orders": "Charging Balance Orders",
        "purchase_orders": "Purchase Orders",
        "api_purchase_orders": "Instant Purchase Orders ⚡",
        "order_details_text": "Order Details",
        "order_id": "Order ID",
        "order_status": "Order Status",
        "order_amount": "Amount",
        "order_date": "Order Date",
        "payment_method": "Payment Method",
        "payment_address": "Payment Address",
        "payment_proof": "Payment Proof",
        "game_account_id": "Game Account ID",
        "item_name": "Item Name",
        "game_name": "Game Name",
        "order_status_pending": "Pending",
        "order_status_processing": "Processing",
        "order_status_completed": "Completed",
        "order_status_cancelled": "Cancelled",
        "order_status_refunded": "Refunded",
        "order_status_failed": "Failed",
        "insufficient_balance": (
            "Insufficient balance ❌\n"
            "Your current balance: {balance} SDG\n"
            "Required price: {price} SDG"
        ),
        "insufficient_balance_charge": (
            "Insufficient balance ❌\n"
            "Your current balance: {balance} SDG\n"
            "Required price: {price} SDG\n\n"
            "Please charge your balance first 💰"
        ),
        "item_not_found": "Item not found or inactive ❌",
        "order_not_found": "Order not found ❌",
        "admin_notes": "Admin Notes",
        "select_order": "Select an order to view:",
        "orders_settings": "Orders Management 📋",
        "orders_settings_title": "Orders Management 📋",
        # General Settings
        "general_settings_title": "General Settings ⚙️",
        "api_provider_settings_title": "Select active provider (only one at a time):\n\nCurrent: {provider}",
        "api_provider_updated": "Provider updated ✅",
        "api_provider_switch_warning": "Provider updated. Re-check Filter API Games for the new catalog. Pending orders keep their original provider.",
        "api_provider": "Provider",
        "api_provider_g2bulk": "G2Bulk",
        "api_provider_gamevouchers": "Game Vouchers",
        "voucher_codes": "Voucher Codes",
        "order_async_hint": "Your order is processing. You will be notified when it completes.",
        "current_usd_to_sudan_rate": "Current Exchange Rate: <code>{rate}</code>",
        "enter_usd_to_sudan_rate": (
            "Enter USD to Sudan Currency exchange rate:\n"
            "Current rate: <code>{current_rate}</code>"
        ),
        "invalid_rate": "Invalid rate ❌\nMust be a positive number",
        "rate_updated_success": (
            "Exchange rate updated successfully ✅\n" "New rate: <code>{rate}</code>"
        ),
        "change_status": "Change Status",
        "add_notes": "Add Notes",
        "select_order_status": "Select order status:",
        "enter_order_notes": "Enter notes for this order:",
        "order_notes_added": "Notes added successfully ✅",
        "reply_to_order_for_notes": "📝 Reply to the order message above to add notes to this order.",
        "reply_to_order_for_amount": "💰 Reply to the order message above with the new amount (number only).",
        "notes_empty": "Notes cannot be empty ❌",
        "order_not_found_in_reply": "Could not identify the order from the replied message. Please use the 'Add Notes' button on the order message.",
        "order_amount_updated": "Amount updated successfully ✅\nOld amount: {old_amount} SDG\nNew amount: {new_amount} SDG",
        "edit_amount": "Edit Amount",
        "order_status_updated": "Order status updated ✅",
        "charging_order_status_changed": "🔔 <b>Charging Balance Order Status Updated</b>\n\n",
        "purchase_order_status_changed": "🔔 <b>Purchase Order Status Updated</b>\n\n",
        "user": "User",
        "user_id": "User ID",
        "username": "Username",
        "name": "Name",
        "not_available": "N/A",
        "orders_settings": "Orders Management 📋",
        "orders_settings_title": "Orders Management 📋",
        "change_status": "Change Status",
        "add_notes": "Add Notes",
        "select_order_status": "Select order status:",
        "enter_order_notes": "Enter notes for this order:",
        "order_notes_added": "Notes added successfully ✅",
        "reply_to_order_for_notes": "📝 Reply to the order message above to add notes to this order.",
        "reply_to_order_for_amount": "💰 Reply to the order message above with the new amount (number only).",
        "notes_empty": "Notes cannot be empty ❌",
        "order_not_found_in_reply": "Could not identify the order from the replied message. Please use the 'Add Notes' button on the order message.",
        "order_amount_updated": "Amount updated successfully ✅\nOld amount: {old_amount} SDG\nNew amount: {new_amount} SDG",
        "edit_amount": "Edit Amount",
        "order_status_updated": "Order status updated ✅",
        "order_already_assigned": "⚠️ This order is being handled by another admin",
        "order_status_terminal": "⚠️ Cannot change order status as it is in a terminal state",
        "user": "User",
        "no_pending_orders": "No pending or processing orders found ❗️",
        "select_game_api": "Select game for instant purchase:",
        "search_game_hint": "\n\n💡 You can also type the game name to search",
        # Instant Purchase (API)
        "loading_game_catalog": "Loading catalog...",
        "select_denomination": "Select denomination:",
        "no_search_results": "❌ No results found",
        "search_results": "🔍 Search results:",
        "enter_player_id": "Enter Player ID:",
        "enter_server_id": "Enter Server ID:",
        "validating_player_id": "Validating player ID...",
        "player_id_valid": "Player ID validated ✅\nName: {player_name}",
        "player_id_invalid": "Invalid player ID ❌",
        "server_not_required": "This game does not require a server",
        "confirm_order": "Confirm Order",
        "order_processing": "Processing order...",
        "order_created_success": "Order created successfully ✅\nOrder ID: {order_id}",
        "order_created_error": "Error creating order ❌\n{error}",
        "insufficient_balance_api": "Insufficient balance ❌\nYour balance: {balance}\nRequired price: {price}",
        "product_out_of_stock": "This product is currently out of stock ❌\nWe apologize for the inconvenience",
        "no_games_available": "No games available at the moment ❗️",
        "no_filtered_games_available": "No games available. Please contact admin.",
        "game_not_available": "This game is not available",
        "no_denominations_available": "No denominations available for this game ❗️",
        # API Purchase Order Statuses
        "api_order_status_pending": "Pending",
        "api_order_status_processing": "Processing",
        "api_order_status_completed": "Completed",
        "api_order_status_failed": "Failed",
        "api_order_status_cancelled": "Cancelled",
        "api_order_completed": "Your order has been completed successfully!",
        "api_order_failed": "Your order has failed.",
        "api_order_cancelled": "Your order has been cancelled.",
        "balance_refunded": "Your balance has been refunded: {amount} SDG",
        "api_order_id": "API Order ID",
        "player_id": "Player ID",
        "player_name": "Player Name",
        "denomination": "Denomination",
        "server_id": "Server ID",
        "message": "Message",
        "remark": "Remark",
        "api_error": "Error connecting to service ❌",
        "order_confirm_summary": (
            "<b>Confirm your order</b>\n\n"
            "🎮 <b>Game:</b> {game_name}\n"
            "📦 <b>Product:</b> {denomination}\n"
            "{quantity_line}"
            "💰 <b>Price:</b> <code>{price} SDG</code>\n"
            "{player_line}"
            "{server_line}\n"
            "💳 <b>Your balance:</b> <code>{balance} SDG</code>\n\n"
            "Press <b>Confirm</b> to place the order, or <b>Cancel</b> to exit without charging your balance."
        ),
        "order_confirm_quantity_line": "🔢 <b>Quantity:</b> {quantity}\n",
        "enter_quantity": "Enter quantity (1-{max}):",
        "invalid_quantity": "Invalid quantity. Enter a number from 1 to {max}.",
        "voucher_quantity_details_text": (
            "<b>Product Details:</b>\n\n"
            "🎮 <b>Game:</b> {game_name}\n"
            "📦 <b>Product:</b> {denomination}\n"
            "💰 <b>Unit price:</b> <code>{unit_price}</code> SDG\n\n"
            "{enter_quantity}"
        ),
        "api_purchase_cancelled_no_charge": "Order cancelled. No balance was deducted ✅",
        "player_id_required": "Player ID is required for this product ❗️",
        "order_details_header": "Order Details:\n",
        "order_details": (
            "Order Details:\n"
            "Game: <b>{game_name}</b>\n"
            "Denomination: <b>{denomination}</b>\n"
            "Price: <code>{price}</code> SDG\n"
            "Player ID: <code>{player_id}</code>\n"
            "Current Balance: <code>{balance}</code>"
        ),
        "manual_order_details": (
            "Order Details:\n"
            "Status: {status}\n"
            "Item: <b>{item_name}</b>\n"
            "Game: <b>{game_name}</b>\n"
            "Price: <code>{price}</code> SDG\n"
            "Game Account ID: <code>{game_account_id}</code>\n"
            "Current Balance: <code>{balance}</code> SDG"
        ),
        "product_details": "Product Details 📦",
        "product_details_text": (
            "<b>Product Details:</b>\n\n"
            "🎮 <b>Game:</b> {game_name}\n"
            "📦 <b>Denomination:</b> {denomination}\n"
            "💰 <b>Price:</b> <code>{price}</code> SDG\n\n"
            "{enter_player_id}"
        ),
        # Filter API Games
        "filter_api_games_settings_title": "Filter API Games Settings 🔍",
        "select_api_game_to_manage": "Select a game to manage:",
        "api_games_list_info": "🟢 = Game exists and is active\n🔴 = Game doesn't exist or is inactive",
        "enter_arabic_name": "Enter the Arabic name for this game:",
        "arabic_name_saved": "Arabic name saved successfully ✅",
        "api_game_status_updated": "Game status updated successfully ✅",
        "set_arabic_name": "Set Arabic Name",
        "toggle_api_game_status": "Toggle Status",
        "original_name": "Original Name",
        "arabic_name": "Arabic Name",
        "select_filtered_game_to_manage": "Select a filtered game to manage:",
        "filtered_games_list_info": "🟢 = Active\n🔴 = Inactive",
        "no_filtered_games": "No filtered games found. Please filter games from API first.",
        "game_not_found": "Game not found",
        "order_user_info": "Order's user info",
    },
}

BUTTONS = {
    models.Language.ARABIC: {
        "check_joined": "تحقق ✅",
        "bot_channel": "قناة البوت 📢",
        "bot_chat": "محادثة البوت 💬",
        "back_button": "الرجوع 🔙",
        "next_button": "التالي",
        "settings": "الإعدادات ⚙️",
        "lang": "اللغة 🌐",
        "back_to_home_page": "العودة إلى القائمة الرئيسية 🔙",
        "select_admin_button": "اختيار حساب آدمن",
        "select_user_button": "اختيار حساب مستخدم",
        "unban_button": "فك الحظر 🔓",
        "ban_button": "حظر 🔒",
        "add_admin": "إضافة آدمن ➕",
        "remove_admin": "حذف آدمن ✖️",
        "show_admins": "عرض الآدمنز الحاليين 👓",
        "admin_settings": "إعدادات الآدمن 🎛",
        "ban_unban": "حظر/فك حظر 🔓🔒",
        "hide_ids_keyboard": "إخفاء/إظهار كيبورد معرفة الآيديات🪄",
        "broadcast": "رسالة جماعية 👥",
        "everyone": "الجميع 👥",
        "specific_users": "مستخدمين محددين 👤",
        "all_users": "جميع المستخدمين 👨🏻‍💼",
        "all_admins": "جميع الآدمنز 🤵🏻",
        "channel_or_group": "قناة أو مجموعة 📢",
        "force_join_chats": "محادثات الإجبار على الانضمام 💬",
        "force_join_chats_settings": "إعدادات محادثات الإجبار على الانضمام 💬",
        "add_force_join_chat": "إضافة محادثة ➕",
        "remove_force_join_chat": "حذف محادثة ✖️",
        "show_force_join_chats": "عرض المحادثات 👓",
        "select_chat_button": "اختيار محادثة",
        "confirm_button": "تأكيد ✅",
        "cancel_order_button": "إلغاء ❌",
        "bot": "بوت 🤖",
        "channel": "قناة 📢",
        "group": "مجموعة 👥",
        "user": "مستخدم 🆔",
        "manage_permissions": "إدارة الصلاحيات 🔐",
        "edit_permissions": "تعديل الصلاحيات ✏️",
        "skip_button": "تخطي ⬅️",
        "save_button": "حفظ ✅",
        "permission_ban_users": "حظر/فك حظر المستخدمين",
        "permission_broadcast": "إرسال رسائل جماعية",
        "permission_manage_force_join": "إدارة محادثات الإجبار على الانضمام",
        "permission_view_ids": "عرض معرفات المستخدمين/المحادثات",
        "permission_manage_permissions": "إدارة الصلاحيات",
        "permission_manage_admins": "إدارة الآدمنز",
        "permission_manage_users": "إدارة المستخدمين",
        "permission_manage_games": "إدارة الألعاب",
        "permission_manage_items": "إدارة العناصر",
        "permission_manage_payment_methods": "إدارة طرق الدفع",
        "permission_manage_orders": "إدارة الطلبات",
        "permission_manage_general_settings": "إدارة الإعدادات العامة",
        "permission_filter_api_games": "تصفية ألعاب API",
        "manage_users_settings": "إدارة المستخدمين 👥",
        "filter_api_games_settings": "تصفية ألعاب API 🔍",
        "filter_api_games": "تصفية ألعاب API 🔍",
        "manage_filtered_games": "إدارة الألعاب المصفاة 📋",
        "orders_settings": "إدارة الطلبات 📋",
        "orders_settings_title": "إدارة الطلبات 📋",
        # General Settings
        "general_settings": "الإعدادات العامة ⚙️",
        "usd_to_sudan_rate": "سعر صرف الدولار إلى العملة السودانية",
        "api_provider_settings": "المزود",
        "change_status": "تغيير الحالة",
        "add_notes": "إضافة ملاحظات",
        "select_order_status": "اختر حالة الطلب:",
        "enter_order_notes": "أدخل الملاحظات لهذا الطلب:",
        "order_notes_added": "تمت إضافة الملاحظات بنجاح ✅",
        "order_status_updated": "تم تحديث حالة الطلب بنجاح ✅",
        "user": "المستخدم",
        "export_users_to_excel": "تصدير المستخدمين إلى Excel 📊",
        "edit_user_balance": "تعديل رصيد المستخدم",
        "add_deduct_balance": "إضافة/خصم مبلغ",
        "set_new_balance": "تعيين رصيد جديد",
        "zero_balance": "تصفير الرصيد",
        "games_settings": "إعدادات الألعاب 🎮",
        "items_settings": "إعدادات العناصر 🎯",
        "payment_methods_settings": "إعدادات طرق الدفع 💳",
        "orders_settings": "إدارة الطلبات 📋",
        # Games Settings Buttons
        "add_game": "إضافة لعبة ➕",
        "remove_game": "حذف لعبة ✖️",
        "show_games": "عرض الألعاب 👓",
        "edit_game": "تعديل لعبة ✏️",
        # Items Settings Buttons
        "add_item": "إضافة عنصر ➕",
        "remove_item": "حذف عنصر ✖️",
        "show_items": "عرض العناصر 👓",
        "edit_item": "تعديل عنصر ✏️",
        "item_type_game_account": "حساب لعبة",
        "item_type_game_item": "عنصر لعبة",
        "item_type_game_package": "باقة لعبة",
        "item_type_game_boost": "تعزيز لعبة",
        "item_type_other": "أخرى",
        # Payment Methods Settings Buttons
        "add_payment_method": "إضافة طريقة دفع ➕",
        "remove_payment_method": "حذف طريقة دفع ✖️",
        "show_payment_methods": "عرض طرق الدفع 👓",
        "edit_payment_method": "تعديل طريقة دفع ✏️",
        "manage_payment_addresses": "إدارة عناوين الدفع 📍",
        "add_payment_address": "إضافة عنوان دفع ➕",
        "remove_payment_address": "حذف عنوان دفع ✖️",
        "show_payment_addresses": "عرض عناوين الدفع 👓",
        "payment_type_bank_transfer": "تحويل بنكي",
        "payment_type_credit_card": "بطاقة ائتمانية",
        "payment_type_e_wallet": "محفظة إلكترونية",
        "payment_type_crypto": "عملة مشفرة",
        "payment_type_mobile_money": "نقود محمولة",
        "payment_type_other": "أخرى",
        # User Buttons
        "purchase_order": "طلب شراء 🛒",
        "instant_purchase": "شراء فوري ⚡",
        "profile": "الملف الشخصي 👤",
        "charge_balance": "شحن الرصيد 💰",
        "my_orders": "طلباتي 📋",
        "charging_balance_orders": "طلبات شحن الرصيد",
        "purchase_orders": "طلبات الشراء",
        "orders_settings": "إدارة الطلبات 📋",
        "change_status": "تغيير الحالة",
        "add_notes": "إضافة ملاحظات",
        "request_charging_order": "طلب شحن رصيد ⚡",
        "request_purchase_order": "طلب شراء ⚡",
        "api_purchase_orders": "طلبات الشراء الفورية ⚡",
        "edit_amount": "تعديل المبلغ",
        "support": "الدعم 💬",
    },
    models.Language.ENGLISH: {
        "check_joined": "Verify ✅",
        "bot_channel": "Bot's Channel 📢",
        "bot_chat": "Bot's Chat 💬",
        "back_button": "Back 🔙",
        "next_button": "Next",
        "settings": "Settings ⚙️",
        "lang": "Language 🌐",
        "back_to_home_page": "Back to home page 🔙",
        "select_admin_button": "Select Admin Account",
        "select_user_button": "Select User Account",
        "unban_button": "Unban 🔓",
        "ban_button": "Ban 🔒",
        "add_admin": "Add Admin ➕",
        "remove_admin": "Remove Admin ✖️",
        "show_admins": "Show Current Admins 👓",
        "admin_settings": "Admin Settings 🎛",
        "ban_unban": "Ban/Unban 🔓🔒",
        "hide_ids_keyboard": "Hide/Show ID Keyboard🪄",
        "broadcast": "Broadcast Message 👥",
        "everyone": "Everyone 👥",
        "specific_users": "Specific Users 👤",
        "all_users": "All Users 👨🏻‍💼",
        "all_admins": "All Admins 🤵🏻",
        "channel_or_group": "Channel or Group 📢",
        "force_join_chats": "Force Join Chats 💬",
        "force_join_chats_settings": "Force Join Chats Settings 💬",
        "add_force_join_chat": "Add Chat ➕",
        "remove_force_join_chat": "Remove Chat ✖️",
        "show_force_join_chats": "Show Chats 👓",
        "select_chat_button": "Select Chat",
        "confirm_button": "Confirm ✅",
        "cancel_order_button": "Cancel ❌",
        "bot": "Bot 🤖",
        "channel": "Channel 📢",
        "group": "Group 👥",
        "user": "User 🆔",
        "manage_permissions": "Manage Permissions 🔐",
        "edit_permissions": "Edit Permissions ✏️",
        "skip_button": "Skip ⬅️",
        "save_button": "Save ✅",
        "permission_ban_users": "Ban/Unban Users",
        "permission_broadcast": "Broadcast Messages",
        "permission_manage_force_join": "Manage Force Join Chats",
        "permission_view_ids": "View User/Chat IDs",
        "permission_manage_permissions": "Manage Permissions",
        "permission_manage_admins": "Manage Admins",
        "permission_manage_users": "Manage Users",
        "permission_manage_games": "Manage Games",
        "permission_manage_items": "Manage Items",
        "permission_manage_payment_methods": "Manage Payment Methods",
        "permission_manage_general_settings": "Manage General Settings",
        "permission_filter_api_games": "Filter API Games",
        "manage_users_settings": "Manage Users 👥",
        # General Settings
        "general_settings": "General Settings ⚙️",
        "usd_to_sudan_rate": "USD to Sudan Currency Exchange Rate",
        "api_provider_settings": "Provider",
        "api_provider_g2bulk": "G2Bulk",
        "api_provider_gamevouchers": "Game Vouchers",
        "export_users_to_excel": "Export Users to Excel 📊",
        "games_settings": "Games Settings 🎮",
        "items_settings": "Items Settings 🎯",
        "payment_methods_settings": "Payment Methods Settings 💳",
        # Games Settings Buttons
        "add_game": "Add Game ➕",
        "remove_game": "Remove Game ✖️",
        "show_games": "Show Games 👓",
        "edit_game": "Edit Game ✏️",
        # Items Settings Buttons
        "add_item": "Add Item ➕",
        "remove_item": "Remove Item ✖️",
        "show_items": "Show Items 👓",
        "edit_item": "Edit Item ✏️",
        "item_type_game_account": "Game Account",
        "item_type_game_item": "Game Item",
        "item_type_game_package": "Game Package",
        "item_type_game_boost": "Game Boost",
        "item_type_other": "Other",
        # Payment Methods Settings Buttons
        "add_payment_method": "Add Payment Method ➕",
        "remove_payment_method": "Remove Payment Method ✖️",
        "show_payment_methods": "Show Payment Methods 👓",
        "edit_payment_method": "Edit Payment Method ✏️",
        "manage_payment_addresses": "Manage Payment Addresses 📍",
        "add_payment_address": "Add Payment Address ➕",
        "remove_payment_address": "Remove Payment Address ✖️",
        "show_payment_addresses": "Show Payment Addresses 👓",
        "payment_type_bank_transfer": "Bank Transfer",
        "payment_type_credit_card": "Credit Card",
        "payment_type_e_wallet": "E-Wallet",
        "payment_type_crypto": "Cryptocurrency",
        "payment_type_mobile_money": "Mobile Money",
        "payment_type_other": "Other",
        # User Buttons
        "purchase_order": "Purchase Order 🛒",
        "instant_purchase": "Instant Purchase ⚡",
        "profile": "Profile 👤",
        "charge_balance": "Charge Balance 💰",
        "my_orders": "My Orders 📋",
        "charging_balance_orders": "Charging Balance Orders",
        "purchase_orders": "Purchase Orders",
        "orders_settings": "Orders Management 📋",
        "change_status": "Change Status",
        "add_notes": "Add Notes",
        "request_charging_order": "Request Charging Order ⚡",
        "request_purchase_order": "Request Purchase Order ⚡",
        # Filter API Games
        "filter_api_games_settings": "Filter API Games 🔍",
        "filter_api_games": "Filter API Games 🔍",
        "manage_filtered_games": "Manage Filtered Games 📋",
        "api_purchase_orders": "Instant Purchase Orders ⚡",
        "edit_amount": "Edit Amount",
        "support": "Support 💬",
    },
}


def get_lang(user_id: int):
    with models.session_scope() as s:
        return s.get(models.User, user_id).lang
