from flask import Flask, jsonify,request
import pandas as pd
import requests
import wget
import os
import subprocess 
from bs4 import BeautifulSoup
import roman
from collections import OrderedDict
import json
from googletrans import Translator
import pycountry

import pycountry

def get_country_with_language(language_code):
    for country in pycountry.countries:
        if language_code in country.languages:
            return country.name
    return None
translator = Translator()
def detect(text):
    
    result = translator.detect(text)
    return result.lang[:2]
lgs1=[
    {"country_code": "af", "country_name": "Afghanistan", "autres_questions_translation": "Autres questions"},
    {"country_code": "al", "country_name": "Albania", "autres_questions_translation": "Pyetje të tjera"},
    {"country_code": "dz", "country_name": "Algeria", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "as", "country_name": "American Samoa", "autres_questions_translation": "Fa'amaumauga ese"},
    {"country_code": "ad", "country_name": "Andorra", "autres_questions_translation": "Altres preguntes"},
    {"country_code": "ao", "country_name": "Angola", "autres_questions_translation": "Outras perguntas"},
    {"country_code": "ai", "country_name": "Anguilla", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "aq", "country_name": "Antarctica", "autres_questions_translation": "Autres questions"},
    {"country_code": "ag", "country_name": "Antigua and Barbuda", "autres_questions_translation": "Other questions"},
    {"country_code": "ar", "country_name": "Argentina", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "am", "country_name": "Armenia", "autres_questions_translation": "Այլ հարցեր"},
    {"country_code": "aw", "country_name": "Aruba", "autres_questions_translation": "Otros cuestiones"},
    {"country_code": "au", "country_name": "Australia", "autres_questions_translation": "Autres questions"},
    {"country_code": "at", "country_name": "Austria", "autres_questions_translation": "Andere Fragen"},
    {"country_code": "az", "country_name": "Azerbaijan", "autres_questions_translation": "Başqa suallar"},
    {"country_code": "bs", "country_name": "Bahamas", "autres_questions_translation": "Other questions"},
    {"country_code": "bh", "country_name": "Bahrain", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "bd", "country_name": "Bangladesh", "autres_questions_translation": "অন্যান্য প্রশ্ন"},
    {"country_code": "bb", "country_name": "Barbados", "autres_questions_translation": "Other questions"},
    {"country_code": "by", "country_name": "Belarus", "autres_questions_translation": "Іншыя пытанні"},
    {"country_code": "be", "country_name": "Belgium", "autres_questions_translation": "Andere vragen"},
    {"country_code": "bz", "country_name": "Belize", "autres_questions_translation": "Otros cuestiones"},
    {"country_code": "bj", "country_name": "Benin", "autres_questions_translation": "Autres questions"},
    {"country_code": "bm", "country_name": "Bermuda", "autres_questions_translation": "Other questions"},
    {"country_code": "bt", "country_name": "Bhutan", "autres_questions_translation": "ང་ཚོའི་དྲིལ་འཛིན་ཚུ་"},
    {"country_code": "bo", "country_name": "Bolivia", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "bq", "country_name": "Bonaire", "autres_questions_translation": "Other questions"},
    {"country_code": "ba", "country_name": "Bosnia and Herzegovina", "autres_questions_translation": "Druga pitanja"},
    {"country_code": "bw", "country_name": "Botswana", "autres_questions_translation": "Dikgwebo tse dingwe"},
    {"country_code": "bv", "country_name": "Bouvet Island", "autres_questions_translation": "Andre spørsmål"},
    {"country_code": "br", "country_name": "Brazil", "autres_questions_translation": "Outras perguntas"},
    {"country_code": "bn", "country_name": "Brunei Darussalam", "autres_questions_translation": "Pertanyaan lain"},
    {"country_code": "bg", "country_name": "Bulgaria", "autres_questions_translation": "Други въпроси"},
    {"country_code": "bf", "country_name": "Burkina Faso", "autres_questions_translation": "Autres questions"},
    {"country_code": "bi", "country_name": "Burundi", "autres_questions_translation": "Autres questions"},
    {"country_code": "kh", "country_name": "Cambodia", "autres_questions_translation": "សំនួរ​ផ្សេងៗ"},
    {"country_code": "cm", "country_name": "Cameroon", "autres_questions_translation": "Autres questions"},
    {"country_code": "ca", "country_name": "Canada", "autres_questions_translation": "Autres questions"},
    {"country_code": "cv", "country_name": "Cape Verde", "autres_questions_translation": "Outras perguntas"},
    {"country_code": "ky", "country_name": "Cayman Islands", "autres_questions_translation": "Other questions"},
    {"country_code": "cf", "country_name": "Central African Republic", "autres_questions_translation": "Autres questions"},
    {"country_code": "td", "country_name": "Chad", "autres_questions_translation": "Autres questions"},
    {"country_code": "cl", "country_name": "Chile", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "cn", "country_name": "China", "autres_questions_translation": "其他问题"},
    {"country_code": "cx", "country_name": "Christmas Island", "autres_questions_translation": "Other questions"},
    {"country_code": "cc", "country_name": "Cocos (Keeling) Islands", "autres_questions_translation": "Other questions"},
    {"country_code": "co", "country_name": "Colombia", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "km", "country_name": "Comoros", "autres_questions_translation": "Questions et autres"},
    {"country_code": "cg", "country_name": "Congo", "autres_questions_translation": "Autres questions"},
    {"country_code": "ck", "country_name": "Cook Islands", "autres_questions_translation": "Ete auti ete"},
    {"country_code": "cr", "country_name": "Costa Rica", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "ci", "country_name": "Cote D'ivoire", "autres_questions_translation": "Autres questions"},
    {"country_code": "hr", "country_name": "Croatia", "autres_questions_translation": "Druga pitanja"},
    {"country_code": "cu", "country_name": "Cuba", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "cw", "country_name": "Curaçao", "autres_questions_translation": "Otros cuestiones"},
    {"country_code": "cy", "country_name": "Cyprus", "autres_questions_translation": "Άλλες ερωτήσεις"},
    {"country_code": "cz", "country_name": "Czech Republic", "autres_questions_translation": "Další otázky"},
    {"country_code": "cd", "country_name": "Democratic Rep Congo", "autres_questions_translation": "Autres questions"},
    {"country_code": "dk", "country_name": "Denmark", "autres_questions_translation": "Andre spørgsmål"},
    {"country_code": "dj", "country_name": "Djibouti", "autres_questions_translation": "Autres questions"},
    {"country_code": "dm", "country_name": "Dominica", "autres_questions_translation": "Other questions"},
    {"country_code": "do", "country_name": "Dominican Republic", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "ec", "country_name": "Ecuador", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "eg", "country_name": "Egypt", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "sv", "country_name": "El Salvador", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "gq", "country_name": "Equatorial Guinea", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "er", "country_name": "Eritrea", "autres_questions_translation": "የሌሎች ጥያቄዎች"},
    {"country_code": "ee", "country_name": "Estonia", "autres_questions_translation": "Muud küsimused"},
    {"country_code": "et", "country_name": "Ethiopia", "autres_questions_translation": "ሌሎች ጥያቄዎች"},
    {"country_code": "fk", "country_name": "Falkland Islands (Malvinas)", "autres_questions_translation": "Other questions"},
    {"country_code": "fo", "country_name": "Faroe Islands", "autres_questions_translation": "Aðrar spurningar"},
    {"country_code": "fj", "country_name": "Fiji", "autres_questions_translation": "Ete auti ete"},
    {"country_code": "fi", "country_name": "Finland", "autres_questions_translation": "Muut kysymykset"},
    {"country_code": "fr", "country_name": "France", "autres_questions_translation": "Autres questions"},
    {"country_code": "gf", "country_name": "French Guiana", "autres_questions_translation": "Autres questions"},
    {"country_code": "pf", "country_name": "French Polynesia", "autres_questions_translation": "Autres questions"},
    {"country_code": "tf", "country_name": "French Southern Territories", "autres_questions_translation": "Autres questions"},
    {"country_code": "ga", "country_name": "Gabon", "autres_questions_translation": "Autres questions"},
    {"country_code": "gm", "country_name": "Gambia", "autres_questions_translation": "Other questions"},
    {"country_code": "ge", "country_name": "Georgia", "autres_questions_translation": "სხვა კითხვები"},
    {"country_code": "de", "country_name": "Germany", "autres_questions_translation": "Andere Fragen"},
    {"country_code": "gh", "country_name": "Ghana", "autres_questions_translation": "Other questions"},
    {"country_code": "gi", "country_name": "Gibraltar", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "gr", "country_name": "Greece", "autres_questions_translation": "Άλλες ερωτήσεις"},
    {"country_code": "gl", "country_name": "Greenland", "autres_questions_translation": "Inuusuttut inuup taasisinnaavat"},
    {"country_code": "gd", "country_name": "Grenada", "autres_questions_translation": "Other questions"},
    {"country_code": "gp", "country_name": "Guadeloupe", "autres_questions_translation": "Autres questions"},
    {"country_code": "gu", "country_name": "Guam", "autres_questions_translation": "Other questions"},
    {"country_code": "gt", "country_name": "Guatemala", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "gg", "country_name": "Guernsey", "autres_questions_translation": "Other questions"},
    {"country_code": "gn", "country_name": "Guinea", "autres_questions_translation": "Autres questions"},
    {"country_code": "gw", "country_name": "Guinea-Bissau", "autres_questions_translation": "Perguntas adicionais"},
    {"country_code": "gy", "country_name": "Guyana", "autres_questions_translation": "Other questions"},
    {"country_code": "ht", "country_name": "Haiti", "autres_questions_translation": "Lòt kesyon"},
    {"country_code": "hm", "country_name": "Heard Island and Mcdonald Islands", "autres_questions_translation": "Other questions"},
    {"country_code": "va", "country_name": "Holy See (Vatican City State)", "autres_questions_translation": "Altre domande"},
    {"country_code": "hn", "country_name": "Honduras", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "hk", "country_name": "Hong Kong", "autres_questions_translation": "其他问题"},
    {"country_code": "hu", "country_name": "Hungary", "autres_questions_translation": "Egyéb kérdések"},
    {"country_code": "is", "country_name": "Iceland", "autres_questions_translation": "Aðrar spurningar"},
    {"country_code": "in", "country_name": "India", "autres_questions_translation": "अन्य प्रश्न"},
    {"country_code": "io", "country_name": "Indian Ocean Territory", "autres_questions_translation": "Other questions"},
    {"country_code": "id", "country_name": "Indonesia", "autres_questions_translation": "Pertanyaan lain"},
    {"country_code": "ir", "country_name": "Iran, Islamic Republic of", "autres_questions_translation": "سوالات دیگر"},
    {"country_code": "iq", "country_name": "Iraq", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "ie", "country_name": "Ireland", "autres_questions_translation": "Other questions"},
    {"country_code": "im", "country_name": "Isle of Man", "autres_questions_translation": "Other questions"},
    {"country_code": "il", "country_name": "Israel", "autres_questions_translation": "שאלות נוספות"},
    {"country_code": "it", "country_name": "Italy", "autres_questions_translation": "Altre domande"},
    {"country_code": "jm", "country_name": "Jamaica", "autres_questions_translation": "Other questions"},
    {"country_code": "jp", "country_name": "Japan", "autres_questions_translation": "他の質問"},
    {"country_code": "je", "country_name": "Jersey", "autres_questions_translation": "Other questions"},
    {"country_code": "jo", "country_name": "Jordan", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "kz", "country_name": "Kazakhstan", "autres_questions_translation": "Басқа сұрақтар"},
    {"country_code": "ke", "country_name": "Kenya", "autres_questions_translation": "Maswali mengine"},
    {"country_code": "ki", "country_name": "Kiribati", "autres_questions_translation": "Ete auti ete"},
    {"country_code": "kr", "country_name": "Korea", "autres_questions_translation": "기타 질문"},
    {"country_code": "xk", "country_name": "Kosovo", "autres_questions_translation": "Pyetje të tjera"},
    {"country_code": "kw", "country_name": "Kuwait", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "kg", "country_name": "Kyrgyzstan", "autres_questions_translation": "Башка суроолтор"},
    {"country_code": "la", "country_name": "Lao", "autres_questions_translation": "ຄຳຖາມອື່ນໆ"},
    {"country_code": "lv", "country_name": "Latvia", "autres_questions_translation": "Citi jautājumi"},
    {"country_code": "lb", "country_name": "Lebanon", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "ls", "country_name": "Lesotho", "autres_questions_translation": "Litsebeletso tse ling"},
    {"country_code": "lr", "country_name": "Liberia", "autres_questions_translation": "Other questions"},
    {"country_code": "ly", "country_name": "Libyan Arab Jamahiriya", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "li", "country_name": "Liechtenstein", "autres_questions_translation": "Andere Fragen"},
    {"country_code": "lt", "country_name": "Lithuania", "autres_questions_translation": "Kiti klausimai"},
    {"country_code": "lu", "country_name": "Luxembourg", "autres_questions_translation": "Autres questions"},
    {"country_code": "mo", "country_name": "Macao", "autres_questions_translation": "其他问题"},
    {"country_code": "mk", "country_name": "Macedonia, the Former Yugoslav Republic of", "autres_questions_translation": "Други прашања"},
    {"country_code": "mg", "country_name": "Madagascar", "autres_questions_translation": "Fijerena hafa"},
    {"country_code": "mw", "country_name": "Malawi", "autres_questions_translation": "Zina zina"},
    {"country_code": "my", "country_name": "Malaysia", "autres_questions_translation": "Soalan lain"},
    {"country_code": "mv", "country_name": "Maldives", "autres_questions_translation": "އަހަރެންގެ ސަރުކޮށްގެ"},
    {"country_code": "ml", "country_name": "Mali", "autres_questions_translation": "Autres questions"},
    {"country_code": "mt", "country_name": "Malta", "autres_questions_translation": "Mistoqsijiet oħra"},
    {"country_code": "mh", "country_name": "Marshall Islands", "autres_questions_translation": "Other questions"},
    {"country_code": "mq", "country_name": "Martinique", "autres_questions_translation": "Autres questions"},
    {"country_code": "mr", "country_name": "Mauritania", "autres_questions_translation": "سوالات دیگر"},
    {"country_code": "mu", "country_name": "Mauritius", "autres_questions_translation": "Questions et autres"},
    {"country_code": "yt", "country_name": "Mayotte", "autres_questions_translation": "Autres questions"},
    {"country_code": "mx", "country_name": "Mexico", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "fm", "country_name": "Micronesia, Federated States of", "autres_questions_translation": "Other questions"},
    {"country_code": "md", "country_name": "Moldova, Republic of", "autres_questions_translation": "Alte întrebări"},
    {"country_code": "mc", "country_name": "Monaco", "autres_questions_translation": "Autres questions"},
    {"country_code": "mn", "country_name": "Mongolia", "autres_questions_translation": "Бусад асуулт"},
    {"country_code": "ms", "country_name": "Montserrat", "autres_questions_translation": "Other questions"},
    {"country_code": "ma", "country_name": "Morocco", "autres_questions_translation": "سوالات دیگر"},
    {"country_code": "mz", "country_name": "Mozambique", "autres_questions_translation": "Outras perguntas"},
    {"country_code": "mm", "country_name": "Myanmar", "autres_questions_translation": "အခြားမေးခွန်းများ"},
    {"country_code": "na", "country_name": "Namibia", "autres_questions_translation": "Ander vrae"},
    {"country_code": "nr", "country_name": "Nauru", "autres_questions_translation": "Other questions"},
    {"country_code": "np", "country_name": "Nepal", "autres_questions_translation": "अन्य प्रश्नहरू"},
    {"country_code": "nl", "country_name": "Netherlands", "autres_questions_translation": "Andere vragen"},
    {"country_code": "an", "country_name": "Netherlands Antilles", "autres_questions_translation": "Otros cuestiones"},
    {"country_code": "nc", "country_name": "New Caledonia", "autres_questions_translation": "Autres questions"},
    {"country_code": "nz", "country_name": "New Zealand", "autres_questions_translation": "Other questions"},
    {"country_code": "ni", "country_name": "Nicaragua", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "ne", "country_name": "Niger", "autres_questions_translation": "Autres questions"},
    {"country_code": "ng", "country_name": "Nigeria", "autres_questions_translation": "Other questions"},
    {"country_code": "nu", "country_name": "Niue", "autres_questions_translation": "Other questions"},
    {"country_code": "nf", "country_name": "Norfolk Island", "autres_questions_translation": "Other questions"},
    {"country_code": "mp", "country_name": "Northern Mariana Islands", "autres_questions_translation": "Other questions"},
    {"country_code": "no", "country_name": "Norway", "autres_questions_translation": "Andre spørsmål"},
    {"country_code": "om", "country_name": "Oman", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "pk", "country_name": "Pakistan", "autres_questions_translation": "دیگر سوالات"},
    {"country_code": "pw", "country_name": "Palau", "autres_questions_translation": "Other questions"},
    {"country_code": "ps", "country_name": "Palestinian Territory, Occupied", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "pa", "country_name": "Panama", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "pg", "country_name": "Papua New Guinea", "autres_questions_translation": "Lain pertanyaan"},
    {"country_code": "py", "country_name": "Paraguay", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "pe", "country_name": "Peru", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "ph", "country_name": "Philippines", "autres_questions_translation": "Iba pang mga tanong"},
    {"country_code": "pn", "country_name": "Pitcairn", "autres_questions_translation": "Other questions"},
    {"country_code": "pl", "country_name": "Poland", "autres_questions_translation": "Inne pytania"},
    {"country_code": "pt", "country_name": "Portugal", "autres_questions_translation": "Outras perguntas"},
    {"country_code": "pr", "country_name": "Puerto Rico", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "qa", "country_name": "Qatar", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "re", "country_name": "Reunion", "autres_questions_translation": "Autres questions"},
    {"country_code": "ro", "country_name": "Romania", "autres_questions_translation": "Alte întrebări"},
    {"country_code": "ru", "country_name": "Russian Federation", "autres_questions_translation": "Другие вопросы"},
    {"country_code": "rw", "country_name": "Rwanda", "autres_questions_translation": "Ibindi byinshi"},
    {"country_code": "sh", "country_name": "Saint Helena", "autres_questions_translation": "Autres questions"},
    {"country_code": "kn", "country_name": "Saint Kitts and Nevis", "autres_questions_translation": "Other questions"},
    {"country_code": "lc", "country_name": "Saint Lucia", "autres_questions_translation": "Other questions"},
    {"country_code": "pm", "country_name": "Saint Pierre and Miquelon", "autres_questions_translation": "Other questions"},
    {"country_code": "vc", "country_name": "Saint Vincent", "autres_questions_translation": "Other questions"},
    {"country_code": "ws", "country_name": "Samoa", "autres_questions_translation": "O le isi galuega"},
    {"country_code": "sm", "country_name": "San Marino", "autres_questions_translation": "Other questions"},
    {"country_code": "st", "country_name": "Sao Tome and Principe", "autres_questions_translation": "Outras perguntas"},
    {"country_code": "sa", "country_name": "Saudi Arabia", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "sn", "country_name": "Senegal", "autres_questions_translation": "Autres questions"},
    {"country_code": "rs", "country_name": "Serbia", "autres_questions_translation": "Друга питања"},
    {"country_code": "sc", "country_name": "Seychelles", "autres_questions_translation": "Autres questions"},
    {"country_code": "sl", "country_name": "Sierra Leone", "autres_questions_translation": "Other questions"},
    {"country_code": "sg", "country_name": "Singapore", "autres_questions_translation": "Pertanyaan lain"},
    {"country_code": "sx", "country_name": "Sint Maarten", "autres_questions_translation": "Other questions"},
    {"country_code": "sk", "country_name": "Slovakia", "autres_questions_translation": "Iné otázky"},
    {"country_code": "si", "country_name": "Slovenia", "autres_questions_translation": "Druga vprašanja"},
    {"country_code": "sb", "country_name": "Solomon Islands", "autres_questions_translation": "Other questions"},
    {"country_code": "so", "country_name": "Somalia", "autres_questions_translation": "Su'aalo kale"},
    {"country_code": "za", "country_name": "South Africa", "autres_questions_translation": "Other questions"},
    {"country_code": "gs", "country_name": "South Georgia and the South Sandwich Islands", "autres_questions_translation": "Other questions"},
    {"country_code": "es", "country_name": "Spain", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "lk", "country_name": "Sri Lanka", "autres_questions_translation": "වෙනත් ප්‍රශ්න"},
    {"country_code": "sd", "country_name": "Sudan", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "sr", "country_name": "Suriname", "autres_questions_translation": "Other questions"},
    {"country_code": "sj", "country_name": "Svalbard and Jan Mayen", "autres_questions_translation": "Andre spørsmål"},
    {"country_code": "sz", "country_name": "Swaziland", "autres_questions_translation": "Other questions"},
    {"country_code": "se", "country_name": "Sweden", "autres_questions_translation": "Andra frågor"},
    {"country_code": "ch", "country_name": "Switzerland", "autres_questions_translation": "Andere Fragen"},
    {"country_code": "sy", "country_name": "Syrian Arab Republic", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "tw", "country_name": "Taiwan", "autres_questions_translation": "其他问题"},
    {"country_code": "tj", "country_name": "Tajikistan", "autres_questions_translation": "Саволҳои дигар"},
    {"country_code": "tz", "country_name": "Tanzania", "autres_questions_translation": "Maswali mengine"},
    {"country_code": "th", "country_name": "Thailand", "autres_questions_translation": "คำถามอื่น ๆ"},
    {"country_code": "tl", "country_name": "Timor-Leste", "autres_questions_translation": "Perguntas adicionais"},
    {"country_code": "tg", "country_name": "Togo", "autres_questions_translation": "Autres questions"},
    {"country_code": "tk", "country_name": "Tokelau", "autres_questions_translation": "Other questions"},
    {"country_code": "to", "country_name": "Tonga", "autres_questions_translation": "Fekauʻaki mo e ngaahi fakamoʻoni"},
    {"country_code": "tt", "country_name": "Trinidad and Tobago", "autres_questions_translation": "Other questions"},
    {"country_code": "tn", "country_name": "Tunisia", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "tr", "country_name": "Turkey", "autres_questions_translation": "Diğer sorular"},
    {"country_code": "tm", "country_name": "Turkmenistan", "autres_questions_translation": "Başga soraglar"},
    {"country_code": "tc", "country_name": "Turks and Caicos Islands", "autres_questions_translation": "Other questions"},
    {"country_code": "tv", "country_name": "Tuvalu", "autres_questions_translation": "Fano te mafai"},
    {"country_code": "ug", "country_name": "Uganda", "autres_questions_translation": "Other questions"},
    {"country_code": "ua", "country_name": "Ukraine", "autres_questions_translation": "Інші питання"},
    {"country_code": "ae", "country_name": "United Arab Emirates", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "gb", "country_name": "United Kingdom", "autres_questions_translation": "Other questions"},
    {"country_code": "us", "country_name": "United States", "autres_questions_translation": "Other questions"},
    {"country_code": "um", "country_name": "United States Minor Outlying Islands", "autres_questions_translation": "Other questions"},
    {"country_code": "uy", "country_name": "Uruguay", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "uz", "country_name": "Uzbekistan", "autres_questions_translation": "Boshqa savollar"},
    {"country_code": "vu", "country_name": "Vanuatu", "autres_questions_translation": "Other questions"},
    {"country_code": "ve", "country_name": "Venezuela", "autres_questions_translation": "Otras preguntas"},
    {"country_code": "vn", "country_name": "Vietnam", "autres_questions_translation": "Câu hỏi khác"},
    {"country_code": "vg", "country_name": "Virgin Islands, British", "autres_questions_translation": "Other questions"},
    {"country_code": "vi", "country_name": "Virgin Islands, U.S.", "autres_questions_translation": "Other questions"},
    {"country_code": "wf", "country_name": "Wallis and Futuna", "autres_questions_translation": "Autres questions"},
    {"country_code": "eh", "country_name": "Western Sahara", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "ye", "country_name": "Yemen", "autres_questions_translation": "أسئلة أخرى"},
    {"country_code": "zm", "country_name": "Zambia", "autres_questions_translation": "Zina zina"},
    {"country_code": "zw", "country_name": "Zimbabwe", "autres_questions_translation": "Zvinyorwa zvinyorwa"}
  ]
lgs2={}
lgs3={}
translations=[]
for i in lgs1:
    lgs2[i.get("country_name")]=i.get("country_code")
    lgs3[i.get("country_code")]=i.get("autres_questions_translation")
    igt=i.get("autres_questions_translation")
    if igt not in translations:
        translations.append(igt)
del lgs1        
app = Flask(__name__)
os.chdir("static")
@app.route('/index')
def hello_world():
    return "hello in bahae api"
def extract_titles(soup):
    """Extrait tous les titres h1, h2, h3, h4 de la soupe donnée."""
    titles = []
    for level in range(1, 5):
        for tag in soup.find_all(f'h{level}'):
            titles.append((level, tag.text))
    return titles

def create_table_of_contents(soup):
    # Initialize the table of contents list
    table_of_contents = []
    tag_names = ["h2", "h3", "h4", "h5","h6"]
    indices = [0] * len(tag_names)

    # Loop through each tag name
    for index, tag_name in enumerate(tag_names):
        # Find all occurrences of the tag in the soup
        tags = soup.find_all(tag_name)

        # Loop through each found tag
        for tag in tags:
            # Get the content of the tag
            content = tag.get_text().strip()

            # Find the position of the tag content in the entire HTML content
            position = soup.get_text().find(content)

            # Set the index for the current level of hierarchy
            indices[index] += 1

            # Create the index string for the current tag
            if index == 1:
                index_str = chr(96 + indices[1])
            elif index >= 3:
                index_str = roman.toRoman(indices[index])
            else:
                index_str = str(indices[index])

            # Create a dictionary to store the tag information
            tag_info = {
                "tag_name": tag_name,
                "index": index_str,
                "position": position,
                "content": content
            }

            # Append the tag information to the table of contents list
            table_of_contents.append(tag_info)

            # Reset indices for lower levels of hierarchy
            for j in range(index + 1, len(indices)):
                indices[j] = 0

    return sorted(table_of_contents, key=lambda x: x['position'])
def tbl(soup):
 rt= OrderedDict()  
# Create the table of contents
 table_of_contents = create_table_of_contents(soup)

# Print the table of contents
 niv = int(table_of_contents[0].get('tag_name')[1:])
 debut = "0"
 ii = 0

 for i in table_of_contents:
    nniv = int(i.get('tag_name')[1:])

    if nniv > niv:
        ii += 1
        debut = debut + ".1"
    elif nniv == niv:
        debut = ".".join(debut.split(".")[:-1] + [str(int(debut.split(".")[-1]) + 1)])
    else:
        ii -= 1
        debut = ".".join(debut.split(".")[:-2] + [str(int(debut.split(".")[-2]) + 1)])

    niv = nniv
    def ch(a):
      if len(a)==1:
        return a[0]
      elif len(a)==2:
        return [a[0],chr(96 + int(a[1]))]
      else :
        
        return [a[0],chr(96 + int(a[1])),roman.toRoman(int(a[2]))]+a[3::]
    chh=ch(debut.split("."))
   # rt[i.get('position')]={"position":i.get('position'),"index":'.'.join(chh),"text":i.get('content')}
    rt['.'.join(chh)]=i.get('content')
 return rt 
def extract_table_of_contents(soup):
    """
    Extracts the table of contents from a BeautifulSoup object.
    
    Args:
    - soup: BeautifulSoup object representing the parsed HTML
    
    Returns:
    - table_of_contents (dict): A dictionary representing the table of contents
                                with hierarchical structure based on heading tags
    """
    table_of_contents = {}
    current_level = table_of_contents
    
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    for heading in headings:
        tag_name = heading.name
        title = heading.get_text().strip()
        level = int(tag_name[1])  # Extract the level from the tag name (e.g., 'h1' -> level 1)
        
        # Create a new entry in the table of contents
        current_level[level] = {'title': title, 'subheadings': {}}
        
        # Update the current level based on the hierarchy
        if level == 1:
            current_level = table_of_contents
        else:
            parent_level = level - 1
            # Ensure the parent level exists before accessing it
            if parent_level in current_level:
                current_level = current_level[parent_level]['subheadings']
    
    return table_of_contents 
def extract_title(soup):
    """
    Extracts the title from a BeautifulSoup object.
    
    Args:
    - soup: BeautifulSoup object representing the parsed HTML
    
    Returns:
    - title (str): The text of the title tag, or None if not found
    """
    title_tag = soup.title
    if title_tag:
        return title_tag.get_text().strip()
    else:
        return None    
def extract_meta_tags(soup):
    """
    Extracts meta tags from a BeautifulSoup object.
    
    Args:
    - soup: BeautifulSoup object representing the parsed HTML
    
    Returns:
    - meta_tags (dict): A dictionary containing meta tag names as keys and their content as values,
                        with numerical keys for multiple occurrences of the same tag
    """
    meta_tags = {}
    meta_elements = soup.find_all('meta')
    for i, meta in enumerate(meta_elements, start=1):
        name = meta.get('name', f'meta_{i}')
        content = meta.get('content', '')
        meta_tags[name] = content.strip()
    return meta_tags    
   
def get_html_text(url):
  
   ers= []
   try: 
    prefixes = [ 'https://','http://','https://www.',  'http://www.']
    if "//" in url :   
        prefixes=['']
    for prefix in prefixes:
        
        try:
            if "//" in url :
                testedurl= url
                
            else: 
                testedurl = prefix + url
                
           
            response = requests.get(testedurl, allow_redirects=True)
           
            if response.status_code == 200:
                soup=BeautifulSoup(response.text, features='html.parser')
                ttbl=tbl(soup)
                ttblk=list(ttbl.keys())
                ttblv=list(ttbl.values())
                fj={'status': 'success','h1':soup.find('h1').get_text().strip(),'titles':{"Paragraphe":ttblk,"numrows":len(ttblk),"Title":ttblv,"rows":list(range(2,len(ttblv)+2))},'topic':extract_title(soup),'metas':extract_meta_tags(soup),'final':str(response.url), 'data': soup.get_text()}#,'tst':str(tst),'testedurl':testedurl,'lasturl':str(list(map(lambda a:a.url,response.history))),
                
           #     fj.update(scrape_headings_from_html(soup))
                
                return  jsonify(OrderedDict(list(fj.items())))

        except Exception as e:#requests.RequestException
            print(f"Error occurred while trying {prefix + url}: {e}")
            ers.append(e)
    return jsonify({'status': 'failed','ers':str(ers),'lasturl':'', 'data': '','prefix':'','testedurl':testedurl})
   except Exception as problem:
           return jsonify({'status': 'failed',"error":str(problem),'lasturl':'', 'data': '','prefix':'','testedurl':testedurl})

def get_html(url):
    prefixes = ['http://', 'https://', 'http://www.', 'https://www.']
    
    for prefix in prefixes:
        try:
            response = requests.get(prefix + url)
            if response.status_code == 200:
                return response.text
        except Exception as e:#requests.RequestException
            print(f"Error occurred while trying {prefix + url}: {e}")
    
    return "nothing worked"

def get_people_also_ask(query,location=None,language=None):
    url = f"https://www.google.com/search"
    print(url)
    params = {"q": query}
    if location:
      lgl=lgs2.get(location)  
      if lgl:  
        params["hl"] = lgl 
    if language:
        params["hl"] = language    

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    params["hl"]=detect(query)    
    response = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the div containing the "People also ask" section
    
#    print(div_containing_text.parent.text)
    # Extract the questions from the same div
    questions=[]
    la=""
    err=""
   
    lts=translations.copy()
    lts.insert(0,lgs3.get(params["hl"]))
    for tt in lts:
      try:  
       div_containing_text = soup.find('div', string=tt)   
       qe= [question.text for question in div_containing_text.parent.find_all('div',string=True)if question.text.strip() != tt]   
       questions.extend(qe)  
       break   
      except Exception as eror :
        err=err+"<br>"+str(eror) 
    
    return list(set(questions)),la,err,params

@app.route('/<path:subpath>')
def tasktest(subpath):
 if request.args.get('paa') =="yes":
     qr,lr,errr,p=get_people_also_ask(subpath,location=request.args.get('location'),language=request.args.get('language'))
     
             
     return json.dumps({"err":str(errr),'params':p,"paa":dict(list(enumerate(qr)))}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}#
 else:    
  try:   
   print("-1-",subpath)   
   return get_html_text(subpath)
  except Exception as me:
   return str(me)   
