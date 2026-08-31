import re
from datetime import datetime, timedelta

# O'zbekiston shaharlari, tumanlari va qishloqlari (lotin va kirill)
CITIES = {
    # Toshkent
    'toshkent': 'Toshkent', 'tashkent': 'Toshkent', 'тошкент': 'Toshkent',
    'angren': 'Angren', 'ангрен': 'Angren',
    'bekobod': 'Bekobod', 'бекобод': 'Bekobod',
    'chinoz': 'Chinoz', 'чиноз': 'Chinoz',
    'gazalkent': 'Gazalkent', 'газалкент': 'Gazalkent',
    'keles': 'Keles', 'келес': 'Keles',
    'ohangaron': 'Ohangaron', 'оҳангарон': 'Ohangaron',
    'olmaliq': 'Olmaliq', 'олмалиқ': 'Olmaliq',
    'piskent': 'Piskent', 'пискент': 'Piskent',
    'qibray': 'Qibray', 'қибрй': 'Qibray',
    'quyichirchiq': "Quyichirchiq", 'қуйичирчиқ': "Quyichirchiq",
    'yangiobod': 'Yangiobod', 'янгиобод': 'Yangiobod',
    'yuqorichirchiq': "Yuqorichirchiq", 'юқоричирчиқ': "Yuqorichirchiq",
    'zangiota': 'Zangiota', 'зангиота': 'Zangiota',
    # Samarqand
    'samarqand': 'Samarqand', 'samarkand': 'Samarqand', 'самарқанд': 'Samarqand',
    'bulungur': 'Bulungur', 'булунғур': 'Bulungur',
    'dargʻom': "Dargʻom", 'дарғом': "Dargʻom",
    'jomboy': 'Jomboy', 'жомбой': 'Jomboy',
    'kattaqoʻrgʻon': "Kattaqoʻrgʻon", 'каттақўрғон': "Kattaqoʻrgʻon",
    'narpay': 'Narpay', 'нарпай': 'Narpay',
    'payariq': 'Payariq', 'паяриқ': 'Payariq',
    'pastdargʻom': "Pastdargʻom", 'пастдарғом': "Pastdargʻom",
    'qoʻshrabot': "Qoʻshrabot", 'қўшработ': "Qoʻshrabot",
    'urgut': 'Urgut', 'ургут': 'Urgut',
    'toyloq': 'Toyloq', 'тойлоқ': 'Toyloq',
    # Buxoro
    'buxoro': 'Buxoro', 'bukhara': 'Buxoro', 'бухоро': 'Buxoro',
    'gʻijduvon': "Gʻijduvon", 'ғиждувон': "Gʻijduvon",
    'jondor': 'Jondor', 'жондор': 'Jondor',
    'kogon': 'Kogon', 'когон': 'Kogon',
    'olot': 'Olot', 'олот': 'Olot',
    'qorakoʻl': "Qorakoʻl", 'қоракўл': "Qorakoʻl",
    'qorovulbozor': 'Qorovulbozor', 'қоровулбозор': 'Qorovulbozor',
    'romitan': 'Romitan', 'ромитан': 'Romitan',
    'shofirkon': 'Shofirkon', 'шофиркон': 'Shofirkon',
    'vobkent': 'Vobkent', 'вобкент': 'Vobkent',
    # Xorazm
    'xorazm': 'Xorazm', 'khorezm': 'Xorazm', 'хорази': 'Xorazm',
    'urganch': 'Urganch', 'urgench': 'Urganch', 'урганч': 'Urganch',
    'xiva': 'Xiva', 'khiva': 'Xiva', 'хива': 'Xiva',
    'bogʻot': "Bogʻot", 'бўгот': "Bogʻot",
    'gurlan': 'Gurlan', 'гурлан': 'Gurlan',
    'hazorasp': 'Hazorasp', 'хазарасп': 'Hazorasp',
    'qoʻshkoʻpir': "Qoʻshkoʻpir", 'қўшкўпир': "Qoʻshkoʻpir",
    'shovot': 'Shovot', 'шовот': 'Shovot',
    'xanka': 'Xanka', 'ханка': 'Xanka',
    'yangibozor': 'Yangibozor', 'янгибозор': 'Yangibozor',
    'yangiarik': 'Yangiariq', 'янгиариқ': 'Yangiariq',
    # Qashqadaryo
    'qarshi': 'Qarshi', 'karshi': 'Qarshi', 'қарши': 'Qarshi',
    'shahrisabz': 'Shahrisabz', 'шахрисабз': 'Shahrisabz',
    'kitob': 'Kitob', 'китоб': 'Kitob',
    'koson': 'Koson', 'қосон': 'Koson',
    'muborak': 'Muborak', 'муборак': 'Muborak',
    'yakkabogʻ': "Yakkabogʻ", 'яккабоғ': "Yakkabogʻ",
    'guzor': 'Guzor', 'гузор': 'Guzor',
    'dehqonobod': 'Dehqonobod', 'деҳқонобод': 'Dehqonobod',
    'chiroqchi': 'Chiroqchi', 'чироқчи': 'Chiroqchi',
    'nisan': 'Nishan', 'нишан': 'Nishan',
    'kasbi': 'Kasbi', 'касби': 'Kasbi',
    # Navoiy
    'navoiy': 'Navoiy', 'navoi': 'Navoiy', 'навоий': 'Navoiy',
    'zarafshon': 'Zarafshon', 'зарафшон': 'Zarafshon',
    'xatirchi': 'Xatirchi', 'хатирчи': 'Xatirchi',
    'qiziltepa': 'Qiziltepa', 'қизилтепа': 'Qiziltepa',
    'tomdi': 'Tomdi', 'томди': 'Tomdi',
    'konimex': 'Konimex', 'конимех': 'Konimex',
    'navbaxor': 'Navbahor', 'навбахор': 'Navbahor',
    'nurota': 'Nurota', 'нурота': 'Nurota',
    'karmana': 'Karmana', 'кармана': 'Karmana',
    # Surxondaryo
    'surxondaryo': 'Surxondaryo', 'surkhandarya': 'Surxondaryo', 'сўрхондарё': 'Surxondaryo',
    'termiz': 'Termiz', 'termez': 'Termiz', 'термиз': 'Termiz',
    'denov': "Denov", 'денов': "Denov",
    'jarqoʻrgʻon': "Jarqoʻrgʻon", 'жарқўрғон': "Jarqoʻrgʻon",
    'qumqoʻrgʻon': "Qumqoʻrgʻon", 'қумқўрғон': "Qumqoʻrgʻon",
    'boysun': 'Baysun', 'бойсун': 'Baysun',
    'sariosiyo': 'Sariosiyo', 'сариосиё': 'Sariosiyo',
    'angor': 'Angor', 'ангор': 'Angor',
    'muzrobod': 'Muzrabot', 'музработ': 'Muzrabot',
    'shoʻrchi': "Shoʻrchi", 'шўрчи': "Shoʻrchi",
    'uzaqir': 'Uzun', 'ўзақир': 'Uzun',
    # Sirdaryo
    'sirdaryo': 'Sirdaryo', 'sirdarya': 'Sirdaryo', 'сирдарё': 'Sirdaryo',
    'guliston': 'Guliston', 'gulistan': 'Guliston', 'гулистон': 'Guliston',
    'yangiyer': 'Yangiyer', 'янгиер': 'Yangiyer',
    'shirin': 'Shirin', 'ширин': 'Shirin',
    'sardoba': 'Sardoba', 'сардоба': 'Sardoba',
    'xovos': 'Xovos', 'ховос': 'Xovos',
    'boyovut': 'Boyovut', 'боёвут': 'Boyovut',
    'mehnatobod': 'Mehnatobod', 'меҳнатобод': 'Mehnatobod',
    'mirzaobod': 'Mirzaobod', 'мирзаобод': 'Mirzaobod',
    'oqoltin': "Oqoltin", 'оқолтин': "Oqoltin",
    'sayxunobod': "Sayxunobod", 'сайхунобод': "Sayxunobod",
    # Jizzax
    'jizzax': 'Jizzax', 'jizzakh': 'Jizzax', 'жизак': 'Jizzax',
    'dostlik': 'Doʻstlik', 'дустлик': "Doʻstlik",
    'zomin': 'Zomin', 'зомин': 'Zomin',
    'baxmal': 'Baxmal', 'бахмал': 'Baxmal',
    'forish': 'Forish', 'фориш': 'Forish',
    'arbor': 'Arnasoy', 'арнасай': 'Arnasoy',
    'gallaorol': 'Gallaorol', 'ғаллаорол': 'Gallaorol',
    'yangiobod': 'Yangiobod', 'янгиобод': 'Yangiobod',
    'zarbdor': 'Zarbdor', 'зарбдор': 'Zarbdor',
    'paxtakor': 'Paxtakor', 'пахтакор': 'Paxtakor',
    'mirzachul': 'Mirzachul', 'мирзачўл': 'Mirzachul',
    # Farg'ona
    "farg'ona": "Fargʻona", "fergana": "Fargʻona", 'фарғона': "Fargʻona",
    'quva': "Quva", 'қува': "Quva",
    'quvasoy': "Quvasoy", 'қувасой': "Quvasoy",
    'qoʻqon': "Qoʻqon", 'kokand': "Qoʻqon", 'қўқон': "Qoʻqon",
    'margʻilon': "Margʻilon", 'марғилон': "Margʻilon",
    'rishton': "Rishton", 'риштон': "Rishton",
    'bagʻdod': "Bagʻdod", 'бағдод': "Bagʻdod",
    'beshariq': "Beshariq", 'бешариқ': "Beshariq",
    'buvayda': "Buvayda", 'бувайда': "Buvayda",
    'dangʻara': "Dangʻara", 'данғара': "Dangʻara",
    'furqat': "Furqat", 'фурқат': "Furqat",
    'oltoriq': "Oltiariq", 'олтиариқ': "Oltiariq",
    'sox': "Soʻx", 'сўх': "Soʻx",
    'toshloq': "Toshloq", 'тошлоқ': "Toshloq",
    'uchkoʻprik': "Uchkoʻprik", 'учкўприк': "Uchkoʻprik",
    'yozovon': "Yozyovon", 'ёзёвон': "Yozyovon",
    # Namangan
    'namangan': 'Namangan', 'наманган': 'Namangan',
    'chust': "Chust", 'чўст': "Chust",
    'kosonsoy': "Kosonsoy", 'қосонсой': "Kosonsoy",
    'mingbuloq': "Mingbuloq", 'мингбулоқ': "Mingbuloq",
    'norin': "Norin", 'норин': "Norin",
    'pop': "Pop", 'поп': "Pop",
    'toraqoʻrgʻon': "Toraqoʻrgʻon", 'торақўрғон': "Toraqoʻrgʻon",
    'uychi': "Uychi", 'уйчи': "Uychi",
    'yangiqoʻrgʻon': "Yangiqoʻrgʻon", 'янгиқўрғон': "Yangiqoʻrgʻon",
    'chartak': "Chortoq", 'чортоқ': "Chortoq",
    # Andijon
    'andijon': 'Andijon', 'andijan': 'Andijon', 'андижон': 'Andijon',
    'asaka': "Asaka", 'асака': "Asaka",
    'xonobod': "Xonobod", 'хонобод': "Xonobod",
    'shahrixon': "Shahrixon", 'шахрихон': "Shahrixon",
    'qoʻrgʻontepa': "Qoʻrgʻontepa", 'қўрғонтепа': "Qoʻrgʻontepa",
    'bulogʻboshi': "Buloqboshi", 'булоқбоши': "Buloqboshi",
    'jalolquduq': "Jalaquduq", 'жалақудуқ': "Jalaquduq",
    'marhamat': "Marhamat", 'марҳамат': "Marhamat",
    'oltinkoʻl': "Oltinkoʻl", 'олтинкўл': "Oltinkoʻl",
    'paxtaobod': "Paxtaobod", 'пахтаобод': "Paxtaobod",
    'xoʻjaobod': "Xoʻjaobod", 'хўжаобод': "Xoʻjaobod",
    'ulugʻnor': "Ulugʻnor", 'улуғнор': "Ulugʻnor",
}

# Noto'g'ri yozuvlar lug'ati
MISSPELLINGS = {
    'toshken': 'Toshkent',
    'tashkent': 'Toshkent',
    'тошкент': 'Toshkent',
    'anjan': 'Andijon',
    'andijan': 'Andijon',
    'андижон': 'Andijon',
    'fargona': "Fargʻona",
    "farghona": "Fargʻona",
    "fergana": "Fargʻona",
    'фарғона': "Fargʻona",
    'samarkand': 'Samarqand',
    'самарқанд': 'Samarqand',
    'buxoro': 'Buxoro',
    'бухоро': 'Buxoro',
    'qoqon': "Qoʻqon",
    'kokand': "Qoʻqon",
    'қўқон': "Qoʻqon",
    'qarshi': 'Qarshi',
    'карши': 'Qarshi',
    'guliston': 'Guliston',
    'гулистон': 'Guliston',
    'jizzax': 'Jizzax',
    'жизак': 'Jizzax',
    'navoiy': 'Navoiy',
    'навоий': 'Navoiy',
    'urganch': 'Urganch',
    'урганч': 'Urganch',
    'termiz': 'Termiz',
    'термиз': 'Termiz',
    'xiva': 'Xiva',
    'хива': 'Xiva',
    # Qo'shimcha qilishingiz mumkin
}

def normalize_city_name(text: str) -> str:
    """Matndagi noto'g'ri shahar nomlarini to'g'rilaydi."""
    lower = text.lower()
    for wrong, correct in MISSPELLINGS.items():
        if wrong in lower:
            lower = lower.replace(wrong, correct)
    return lower

def parse_trip_message(text: str) -> dict:
    result = {
        'from_city': None,
        'to_city': None,
        'phone': None,
        'username': None,
        'date': None,
        'time': None,
        'passengers': None
    }

    # Telefon raqam
    phone_pattern = re.compile(r'(\+?998[0-9]{9})|(\d{9})')
    phone_match = phone_pattern.search(text)
    if phone_match:
        result['phone'] = phone_match.group()

    # Username
    username_pattern = re.compile(r'@(\w+)')
    username_match = username_pattern.search(text)
    if username_match:
        result['username'] = '@' + username_match.group(1)

    # Sana
    date_keywords = ['bugun', 'ertaga', 'kecha', 'today', 'tomorrow', 'yesterday', 'inner', '오늘', '내일', '어제']
    for word in date_keywords:
        if word in text.lower():
            result['date'] = word
            break

    # Vaqt
    time_patterns = [
        r'(\d{1,2}):(\d{2})',
        r'soat\s*(\d{1,2})',
        r'(\d{1,2})\s*da',
        r'(\d{1,2})\s*:',
    ]
    for pat in time_patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            if ':' in pat:
                hour = match.group(1)
                minute = match.group(2)
                result['time'] = f"{hour}:{minute}"
            else:
                hour = int(match.group(1))
                if 0 <= hour <= 23:
                    result['time'] = f"{hour:02d}:00"
            break

    # Yo'lovchilar soni
    pass_patterns = [
        r'(\d+)\s*(?:kishi|нафар|odam|people|person|명|人)',
        r'(\d+)\s*ta\s*(?:kishi|odam)',
    ]
    for pat in pass_patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            result['passengers'] = int(match.group(1))
            break
    if not result['passengers']:
        nums = re.findall(r'\b(\d+)\b', text)
        for n in nums:
            val = int(n)
            if 1 <= val <= 10:
                result['passengers'] = val
                break

    # Shaharlarni aniqlash
    # Avval matnni normalizatsiya qilamiz (noto'g'ri yozuvlarni to'g'rilaymiz)
    normalized_text = normalize_city_name(text)
    text_lower = normalized_text.lower()

    # Barcha shaharlarni topamiz
    found_cities = []  # (matndagi so'z, to'liq nom)
    for key, val in CITIES.items():
        if key in text_lower:
            found_cities.append((key, val))

    if found_cities:
        # 1-usul: "dan" va "ga" so'zlari
        from_match = re.search(r'(.+?)\s*(?:dan|дан|->|→|−|–)\s*(.+)', text_lower, re.IGNORECASE)
        if from_match:
            from_part = from_match.group(1).strip()
            to_part = from_match.group(2).strip()
            # from ni topish
            for key, val in CITIES.items():
                if key in from_part:
                    result['from_city'] = val
                    break
            # to ni topish
            to_part_clean = re.sub(r'\s*ga\s*', ' ', to_part).strip()
            for key, val in CITIES.items():
                if key in to_part_clean:
                    result['to_city'] = val
                    break
        else:
            # "ga" so'zi bo'yicha
            ga_match = re.search(r'(.+?)\s*ga\s*(.+)', text_lower, re.IGNORECASE)
            if ga_match:
                before = ga_match.group(1).strip()
                after = ga_match.group(2).strip()
                for key, val in CITIES.items():
                    if key in before:
                        result['from_city'] = val
                    if key in after:
                        result['to_city'] = val
                # Agar from topilmasa, boshqa shaharni qidirish
                if not result['from_city']:
                    for key, val in CITIES.items():
                        if key in text_lower and key not in after:
                            result['from_city'] = val
                            break
            else:
                # Faqat shaharlarni ketma-ketlikda olish
                unique_cities = []
                seen = set()
                for key, val in found_cities:
                    if val not in seen:
                        seen.add(val)
                        unique_cities.append(val)
                if len(unique_cities) >= 2:
                    result['from_city'] = unique_cities[0]
                    result['to_city'] = unique_cities[1]
                elif len(unique_cities) == 1:
                    # Faqat bitta shahar - uni to_city deb olamiz
                    result['to_city'] = unique_cities[0]

        # Agar from bo'lsa-u to bo'lmasa, ikkinchi shaharni topish
        if result['from_city'] and not result['to_city']:
            for key, val in found_cities:
                if val != result['from_city']:
                    result['to_city'] = val
                    break
        # Agar to bo'lsa-u from bo'lmasa, birinchi shaharni from deb olish
        if result['to_city'] and not result['from_city']:
            for key, val in found_cities:
                if val != result['to_city']:
                    result['from_city'] = val
                    break

    return result