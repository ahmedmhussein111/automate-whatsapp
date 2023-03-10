from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

# Replace YOUR_URL with your mongodb url
cluster = MongoClient("mongodb+srv://admin:admin@cluster0.bihtyrb.mongodb.net/?retryWrites=true&w=majority")
db = cluster["bakery"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")[:-2]
    res = MessagingResponse()
    users.insert_one({"number": number, "status": "main", "messages": []})
    user = users.find_one({"number": number})

    try:
        option = int(text)
    except:
        users.update_one(
            {"number": number}, {"$set": {"status": "main"}})
        res.message("0️⃣ لعرض القائمة الرئيسة")
        return str(res)

    if user["status"] == "main":
        if option == 1:
            res.message("*الإستفسار عن القبول بالجامعة*\n"
                        "1️⃣ للقبول بمرحلة البكالوريوس لحملة شهادة الثانوية العامة:\n"
                        "2️⃣ للقبول ببرامج الماجستير والدبلوم العالي:\n"
                        "3️⃣ للقبول ببرنامج بكالوريوس الطب (المسار الثاني) لحملة درجة البكالوريوس في التخصصات المطلوبة:\n"
                        "0️⃣ للرجوع للقائمة السابقة:")
            users.update_one(
                {"number": number}, {"$set": {"status": "UnivApproval"}})
        elif option == 2:
            users.update_one(
                {"number": number}, {"$set": {"status": "StudentInquery"}})
            res.message("*استفسارات طلاب الجامعة*\n"
                        "1️⃣ للإستعلام عن طلب تغيير الحالة الأكاديمية ( الإنسحاب من الجامعة) او الإعتذار عن إكمال الدراسة:\n"
                        "2️⃣ الإستعلام عن المواعيد المحددة لتقديم طلب:\n"
                        "3️⃣ الإستعلام عن حالة الطلب في نظام المعلومات الطلابي:\n"
                        "4️⃣ الإستعلام عن المكافآت:\n"
                        "0️⃣ للرجوع للقائمة السابقة:")
        elif option == 3:
            users.update_one(
                {"number": number}, {"$set": {"status": "GraduatedInquery"}})
            res.message("*استفسارات الخريجين*\n"
                        "1️⃣ لطلب الشهادة المؤقتة:\n"
                        "2️⃣ للإستعلام عن إستلام الوثائق:\n"
                        "3️⃣ لطلب سجل أكاديمي:\n"
                        "4️⃣ للتحقق من وثائق الخريجين:\n"
                        "0️⃣ للرجوع للقائمة السابقة:")
        elif option == 4:
            users.update_one(
                {"number": number}, {"$set": {"status": "OtherInquery"}})
            res.message("*الإستفسارات الأخري*\n"
                         "\n"
                        "الأسئلة الشائعة"
                        "\n"
                        "https://ksau-hs.edu.sa/Arabic/Admission/Pages/FAQs.aspx"
                        "\n"
                        "دليل المستخدم"
                        "\n"
                        "https://ksau-hs.edu.sa/Arabic/Admission/Pages/AdmissionGuide.aspx"
                        )
        elif option == 0:
            mess = res.message(" \n القائمة الرئيسية *عمادة القبول والتسجيل*"
                        "\n"
                        " يرجي إدخال رقم الخدمة بناء علي نوع الإستفسار الخاص بكم:" "\n \n"
                        "1️⃣ للإستفسار عن القبول بالجامعة" "\n"
                        "2️⃣ لإستفسارات طلاب الجامعة" "\n"
                        "3️⃣ لإستفسارات الخريجين" "\n"
                        "4️⃣ للإستفسارات الأخري" "\n")
            mess.media("https://ksau-hs.edu.sa/Arabic/MediaCenter/News/PublishingImages/_w/EventAdmin001_jpg.jpg")
        else:
            res.message(" \n إختيار خاطيء تم الرجوع للقائمة الرئيسية *عمادة القبول والتسجيل*"
                        "\n"
                        " يرجي إدخال رقم الخدمة بناء علي نوع الإستفسار الخاص بكم:" "\n \n"
                        "1️⃣ للإستفسار عن القبول بالجامعة" "\n"
                        "2️⃣ لإستفسارات طلاب الجامعة" "\n"
                        "3️⃣ لإستفسارات الخريجين" "\n"
                        "4️⃣ للإستفسارات الأخري" "\n")
    elif user["status"] == "UnivApproval":
        if option == 1:
            users.update_one(
                {"number": number}, {"$set": {"status": "UnivApproval_1"}})
            res.message("*القبول بمرحلة البكالوريوس لحملة شهادة الثانوية العامة*\n"
                        "1️⃣ للإستفسار عن فترة التقديم :\n"
                        "2️⃣ للإستفسار عن شروط ومعايير القبول والتخصصات المتاحة للقبول:\n"
                        "3️⃣ أواجه مشكلة تقنية في بوابة التقديم الإلكتروني، ما الحل؟:\n"
                        "4️⃣ للإستعلام عن حالة الترشيح:\n"
                         "5️⃣ للإستفسارات الأخري:\n"
                        "0️⃣ للرجوع للقائمة السابقة:")

        elif option == 2:
            users.update_one(
                {"number": number}, {"$set": {"status": "UnivApproval_2"}})
            res.message("*القبول ببرنامج الماجستير والدبلوم العالي*\n"
                        "1️⃣ اختباري اختباري اختباري  :\n"
                        "2️⃣ اختباري اختباري اختباري :\n"
                        "3️⃣ اختباري اختباري اختباري ؟:\n"
                        "4️⃣ اختباري اختباري اختباري :\n"
                        "5️⃣ اختباري اختباري اختباري :\n"
                        "0️⃣ اختباري اختباري اختباري :")

        elif option == 3:
            users.update_one(
                {"number": number}, {"$set": {"status": "UnivApproval_3"}})
            res.message("*القبول ببرنامج بكالوريوس الطب (المسار الثاني) لحملة درجة البكالوريوس في التخصصات المطلوبة*\n"
                        "1️⃣ اختباري اختباري اختباري  :\n"
                        "2️⃣ اختباري اختباري اختباري :\n"
                        "3️⃣ اختباري اختباري اختباري ؟:\n"
                        "4️⃣ اختباري اختباري اختباري :\n"
                        "5️⃣ اختباري اختباري اختباري :\n"
                        "0️⃣ اختباري اختباري اختباري :")
        else:
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            res.message(" \n اهلا وسهلا بكم في *عمادة القبول والتسجيل*"
                        "\n"
                        " يرجي إدخال رقم الخدمة بناء علي نوع الإستفسار الخاص بكم:" "\n \n"
                        "1️⃣ للإستفسار عن القبول بالجامعة" "\n"
                        "2️⃣ لإستفسارات طلاب الجامعة" "\n"
                        "3️⃣ لإستفسارات الخريجين" "\n"
                        "4️⃣ للإستفسارات الأخري" "\n")

    elif option == 0:
        if user["status"] == "UnivApproval" or user["status"] == "StudentInquery" or user["status"] == "GraduatedInquery" or user["status"] == "OtherInquery":
            res.message("القائمة الرئيسية *لعمادة القبول والتسجيل*"
                        "\n"
                        " يرجي إدخال رقم الخدمة بناء علي نوع الإستفسار الخاص بكم:" "\n \n"
                        "1️⃣ للإستفسار عن القبول بالجامعة" "\n"
                        "2️⃣ لإستفسارات طلاب الجامعة" "\n"
                        "3️⃣ لإستفسارات الخريجين" "\n"
                        "4️⃣ للإستفسارات الأخري" "\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})

        elif user["status"] == "UnivApproval_1" or user["status"] == "UnivApproval_2" or user["status"] == "UnivApproval_3":
            res.message("*الإستفسار عن القبول بالجامعة*\n"
                        "1️⃣ للقبول بمرحلة البكالوريوس لحملة شهادة الثانوية العامة:\n"
                        "2️⃣ للقبول ببرامج الماجستير والدبلوم العالي:\n"
                        "3️⃣ للقبول ببرنامج بكالوريوس الطب (المسار الثاني) لحملة درجة البكالوريوس في التخصصات المطلوبة:\n"
                        "0️⃣ للرجوع للقائمة السابقة:")
            users.update_one(
                {"number": number}, {"$set": {"status": "UnivApproval"}})
        else:
            res.message(" \n اهلا وسهلا بكم في *عمادة القبول والتسجيل*"
                        "\n"
                        " يرجي إدخال رقم الخدمة بناء علي نوع الإستفسار الخاص بكم:" "\n \n"
                        "1️⃣ للإستفسار عن القبول بالجامعة" "\n"
                        "2️⃣ لإستفسارات طلاب الجامعة" "\n"
                        "3️⃣ لإستفسارات الخريجين" "\n"
                        "4️⃣ للإستفسارات الأخري" "\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})

    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run()
