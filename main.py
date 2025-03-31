from flet import *
import sqlite3

class Database:
    def __init__(self):
        self.conn=sqlite3.connect('debt.db',check_same_thread=False)
        self.curser=self.conn.cursor()
        self.creat_table()
        #(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((دالة صناعة جدول )))))))))))))))))))))))))))))))))))))))))))))))))
    def creat_table(self):
        self.curser.execute('''CREATE TABLE IF NOT EXISTS debt(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               lname TEXT,
               ldate_send TEXT,
               lmoney TEXT,
               ltreason TEXT,
               ltime   TEXT,
               ldate_up TEXT
               
               )''')
        self.conn.commit()

        #(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((ابضافة عناصر جديدة))))))))))))))))))))))))))))))))))))))))))
    def add_item(self,lname,ldate_send,lmoney,ltreason,ltime,ldate_up):
        self.curser.execute('''
                INSERT INTO debt(lname,ldate_send,lmoney,ltreason,ltime,ldate_up)VALUES(?,?,?,?,?,?)''',
                            (
                              lname.value,
                              ldate_send.value,
                              lmoney.value,
                              ltreason.value,
                              ltime.value,
                              ldate_up.value
                              )
                            )
        self.conn.commit()

    #(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((جلب جميع العناصر من الجدول))))))))))))))))))))))))))))))))))))))))))
    def get_all_items(self):
        self.curser.execute('SELECT * FROM debt')
        self.conn.commit()
        return self.curser.fetchall()
    
    #((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((جلب عنصر من التجدول )))))))))))))))))))))))))))))))))))))))))))))))))))))
    def get_item(self,item_id):
        self.curser.execute('SELECT FROM debt id=?',(item_id))
        self.conn.commit()
        return self.curser.fetchone()
    
    #((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((التعديل علي العناصر المخزنة في الجدول)))))))))))))))))))))))))))))))))))))))))))))))))))))
    def updat_item(self,id,lname,ldate_send,lmoney,ltreason,ltime,ldate_up):
        self.curser.execute('UPDATE debt SET lname=?,ldate_send=?,lmoney=?,lreason=?,ltime=?,ldate_up=? WHERE id =? ',
                            lname,
                            ldate_send,
                            lmoney,
                            ltreason,
                            ltime,
                            ldate_up
                            )
        self.conn.commit()
    def delete_item(self,id):
        
        self.curser.execute('DELETE FROM debt WHERE id =?',(int(id.value),))
        self.conn.commit()
        
        
    
        
#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((كلاس البطافات )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
# class AddCard:
#     def __init__():
#         data=Database.get_all_items()
#         cards = []
#         for person in data:
#             id, lname, ldate_send, lmoney,ltreason, ltime,ldate_up=person
    
#             card_content =Column(
#                 [
#                     ListTile(
#                         title=Text(f"Name :{id}", weight=FontWeight.BOLD),
#                         subtitle=Text(f": {lname} الاسم:"),
#                     ),
#                     Divider(),
#                     Text(f" : {ldate_send} تاريخ الاستدانة"),
#                     Text(f" :دج {lmoney}عدد النقود "),
#                     Text(f'{ltreason} السبب:'),
#                     Text(f'{ltime}المدة المتوقعة '),
#                     Text(f'{ldate_up}تاريخ تاكيد الارجاع:')

#                 ],
#                 spacing=5,
#             )
    
#             card = Card(
#                 content=Container(
#                     content=card_content,
#                     padding=padding.all(10),
#                 ),
#                 margin=margin.all(10),
#             )
#             cards.append(card)
# ((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((الصفحة الأولى: تسجيل الدخول
class LoginPage:
    def __init__(self, page,db):
        self.db=db
        self.page = page
        
        self.username = TextField(label="اسم المستخدم", value="user",bgcolor='white',fill_color=colors.BLUE_600)
        self.password = TextField(label="كلمة المرور", password=True, value="pass",fill_color=colors.BLUE_600)
        self.error_text = Text("", color=colors.RED)

        self.view = View(
            "/",
            [
                Image(src='/loginhaking.jpg',width=370,),
                self.username,
                self.password,
                
                ElevatedButton("تسجيل الدخول", on_click=self.login_clicked),
                self.error_text,
            ],
            bgcolor=colors.PURPLE_300,
            vertical_alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

    # (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((دالة التحقق من تسجيل الدخول
    def login_clicked(self,s):
        if self.username.value == "user" and self.password.value == "pass":
            self.page.go("/home")
        else:
            self.error_text.value = "اسم المستخدم أو كلمة المرور غير صحيحة"
            self.page.update()


# ((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((الصفحة الثانية: الصفحة الرئيسية
class HomePage:
    def __init__(self,page,db):
        self.db=db
        
        self.page = page
        self.lname = TextField(label="الاسم و اللقب",bgcolor='white',fill_color=colors.BLUE_600,rtl=True)
        self.ldate_send = TextField(label=" تاريخ الادانة ",fill_color=colors.BLUE_600,rtl=True)
        self.lmoney = TextField(label="القيمة بالدينار",bgcolor='white',fill_color=colors.BLUE_600,rtl=True)
        self.ltreason = TextField(label="سبب التدين ",bgcolor='white',fill_color=colors.BLUE_600,rtl=True)
        self.ltime= TextField(label="مدة الارجاع",fill_color=colors.BLUE_600,rtl=True)
        self.ldate_up= TextField(label="تاريخ الارجاع",fill_color=colors.BLUE_600,rtl=True)
        self.image=Image(src="/home/kali/Desktop/python/test/fletapp/testall/debt.jpg")
#((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((اضافة الازرار))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
        self.new_add=ElevatedButton('اضافة شخص جديد',expand=5,on_click=self.add_new)
        self.show_add=ElevatedButton('صفحة العرض ',expand=5,on_click=lambda _:page.go('/page2'))
        self.Delet_person=ElevatedButton('مسح',expand=5,bgcolor=colors.RED_300,)
        self.delet_colomn=ElevatedButton('افراغ الحقول',expand=5,on_click=self.clear_empty)
        self.page3=ElevatedButton("الانتقال الي الصفحة 3", on_click=lambda _: page.go("/page3"))
        

        self.view = View(
            "/home",
            [
                AppBar(title=Text("الصفحة الرئيسية"), bgcolor=colors.GREEN,rtl=True),
                Row([
                    Text("غدد الشخاص المدانة", size=20)
                    ],rtl=True),
                self.image,
                self.lname,self.ldate_send,self.lmoney,self.ltreason,self.ltime,self.ldate_up, 
                Row([
                    self.new_add,self.show_add
            ],rtl=True),
                Row([
                   self.delet_colomn,self.Delet_person
                ],rtl=True),
                self.page3
            ],

            bgcolor='#00B700',
            scroll='auto'
            
        )

    def add_new(self,e):
        try:
            self.db.add_item(self.lname,self.ldate_send,self.lmoney,self.ltreason,self.ltime,self.ldate_up)

        except Exception as ex:
            print('Erorr:',ex)

#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((D(دالة افراغ الحقول ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
    def clear_empty(self,e):
        self.lname.value=""
        self.ldate_send.value='' 
        self.lmoney.value=""
        self.ltreason.value=""
        self.ltime.value=""   
        self.ldate_up.value=''
        self.page.update()
    
#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((الصفحة الثالثة: صفحة العرض الاشخاص المدانة 
class Show_Debt_Add_Page:
    def __init__(self,page,db):
        self.db=db
        self.page = page
        self.bt1=ElevatedButton("العودة إلى الصفحة الرئيسية", padding.all(10),margin.all(20),on_click=lambda _: page.go("/home"),bgcolor=colors.GREEN_600)
        self.delet = TextField(label="ادخل الرقم الدي تريد مسحه",bgcolor='white',fill_color=colors.BLUE_600,rtl=True)
        self.bsharch=ElevatedButton('مسح',on_click=self.delete_new)
        
        #((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((صناعة بطافات لعرضها))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
        data=db.get_all_items()
        cards = []
        for person in data:
            id, lname, ldate_send, lmoney,ltreason, ltime,ldate_up=person
    
            card_content =Column(
                [
                    ListTile(
                        title=Text(f"الرقم  :{id}", weight=FontWeight.BOLD,size=30),
                        subtitle=Text(f"الاسم واللقب :    {lname}",size=20,color='white'),
                    ),
                    Divider(),
                    Text(f" تاريخ الاستدانة:    {ldate_send}",color=colors.BLACK,size=20,weight='bold',font_family='CustomFont'),
                    Text(f" عدد النقود:    {lmoney}دج",color=colors.BLACK,size=20,weight='bold',font_family='CustomFont'),
                    Text(f'سبب الاستدانة:    {ltreason}',color=colors.BLACK,size=20,weight='bold',font_family='CustomFont'),
                    Text(f'المدة المتوقعة :    {ltime}  ',color=colors.BLACK,size=20,weight='bold',font_family='CustomFont'),
                    Text(f'تاريخ تاكيد الاسترجاع :    {ldate_up}',color=colors.BLACK,size=20,weight='bold',font_family='CustomFont')

                ],
                
                spacing=5,rtl=True
            )
    
            self.card = Card(
                elevation=10,
                color='#00B700',
                content=Container(
                    content=card_content,
                    padding=padding.all(10),
                    
                ),
                margin=margin.all(10),
            )
            cards.append(self.card)

        self.view = View(
            "/page2",
            [
                AppBar(title=Text("صفحة العرض"), bgcolor=colors.GREEN,rtl=True),
                Row([
                    self.bt1

                ]),
                Row([
                    self.delet
                ]),
                Row([
                    self.bsharch
                ]),
                Column(cards),
                
                
            ],scroll='auto',bgcolor='red'
        )
        self.page.update(),
        
    def delete_new(self,e):
        self.db.delete_item(self.delet)
        self.page.clean()
        self.page.update()
                


#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((الصفحة الرابعة الاشخاص الدين لديهم نقودك 
class Show_Debt_Up_Page:
    def __init__(self,page,db):
        self.db=db
        self.page = page

        self.view = View(
            "/page3",
            [
                AppBar(title=Text("صفحة الديون "), bgcolor=colors.ORANGE,rtl=True),
                Text("هذه هي الصفحة الثالثة!", size=20,rtl=True),
                ElevatedButton("العودة إلى الصفحة الرئيسية", on_click=lambda _: page.go("/home")),
            ],
        )

# (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((الدالة الرئيسية لإدارة التطبيق
def main(page: Page):
    db=Database()
    page.title = "تطبيق الديون"
    page.window.width=390
    page.window.height=720
    page.window.top=0
    page.window.left=1500
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.scroll='auto'
    page.update()

    #((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))) دالة لتغيير الصفحات بناءً على المسار
    def route_change(e):
        page.views.clear()

        if page.route == "/":
            login_page = LoginPage(page,db)
            page.views.append(login_page.view)
            
        elif page.route == "/home":
            home_page = HomePage(page,db)
            page.views.append(home_page.view)
            
        elif page.route == "/page2":
            second_page = Show_Debt_Add_Page(page,db)
            page.views.append(second_page.view)
            
        elif page.route == '/page3':
            up_page=Show_Debt_Up_Page(page,db)
            page.views.append(up_page.view)

        page.update()

    # ((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((دالة للتعامل مع العودة إلى الصفحة السابقة
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        db.go(top_view.route)

    # (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((تعيين الدوال للتعامل مع تغيير المسار
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # ((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((الانتقال إلى الصفحة الرئيسية
    page.go("/")


# تشغيل التطبيق
app(target=main)