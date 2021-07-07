import cx_Oracle
import os
dsn_tns=cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
conn=cx_Oracle.connect(user=r'system', password='India123$', dsn=dsn_tns) 
c=conn.cursor()
global num
num=50
#c.execute('create table sample2(name varchar(20), roll number(10))')
#c.execute('commit')
#c.execute("select * from sample")
#variable=c.fetchall()
#variable=c.fetchone()
#for line in c:
#    print(line)

def cls():
    os.system("clear")


def assign():
    global num
    num= num+1
    return num

def bill(scid):
    #
    print("\nConfirming order........\n")
    #select from orders where cid = scid
    c.execute("select * from orders where cid='%d'",scid)
    for line in c:
                print(line)
    amt=int(input("Enter bill amount"))
    #update in customer tot_spend=tot_spend+%s,amt
    c.execute("update cust set tot_spend=tot_spend+'%d' where cid='%d'",amt,scid)
    c.execute("commit")

def dinfo(scid,oid,dbid):
    ci = input("Enter city:")
    st = input("Enter street:")
    fno = input("Enter Flat no:")
    choice = input("Any landmarks?(Y/N):")
    if(choice=='Y'):
        lan = input("Enter landmark(if any):")
        #del_id=assign
        deli_id=assign()
        #insert into dinfo(city,street,landmark,flat_no,del_id order_id dboy_id) values(city,street,landmark,flat_no,del_id oid dboy_id);
        c.execute("insert into dinfo(landmark,city,street,flat_no,del_id,order_id,dboy_id) values('%s','%s','%s','%s','%d','%d','%d')",lan,ci,st,fno,deli_id,oid,dbid)
    else:
        #insert into dinfo(city,street,flat_no,del_id,order_id,dboy_id) values(city,street,flat_no,del_id oid dboy_id);  
        c.execute("insert into dinfo(city,street,flat_no,del_id,order_id,dboy_id) values('%s','%s','%s','%d','%d','%d')",ci,st,fno,deli_id,oid,dbid)
    c.execute("commit")
    bill(scid)
    
def cart(scid,mc):
    ch=0
    print("What do you want to do?....\n")
    print("1.Add to cart\n2.Delete from cart\n3.View cart\n4.Place order\n5.Exit\n")
    while(True):
        ch = int(input("Enter your choice:\n"))
        if(ch==1):
            mopay = input("Enter mode of payment:")
            orid=assign()
            #insert into cart mop = mopay cid = custid mcode=mc order_id = Assign*****
            c.execute("insert into cart(mcode,mop,cid,order_id) values('%d','%s','%d','%d')",mc,mopay,scid,orid)
            c.execute("commit") 
            break
        elif(ch==2):
            #delete from cart where mcode = mc cid = custid
            c.execute("delete from cart where mcode='%d' and cid='%d'",mc,scid)
            c.execute("commit")
            break
        elif(ch==3):
            #select * from cart where cid=scid;
            c.execute("select * from cart where cid='%d'",scid)
            for line in c:
                print(line)
            break
        elif(ch==4):
            cho = input("Are you sure?(Y/N):")
            if(cho=='Y'):
                #retrieve order_id...oid
                c.execute("select order_id from cart where cid='%d' and mcode='%s'",scid,mc)
                oid=c.fetchone()
                c.execute("select dboy_id from dboy")
                dbid=c.fetchone()
                dinfo(scid,oid,dbid)
            else:
                cart(scid,mc)
            break
        elif(ch==5):
            print("Quitting......\n")
            exit(0)
        else:
            ch=0
            print("Wrong choice........Try again....\n")
            
def cust():
    ch=0
    #login
    name = input("Username:")
    cusid = int(input("Enter id:"))
    c.execute("select cname from cust where cid='%s' and cname='%s'",cusid,name)
    scid=c.fetchone()
    print(scid)
    #scid=retrieve from customer
    print("What do you want to do?....\n")
    print("1.Edit details\n2.View menu\n3.Access cart\n4.Search filter\n5.Feedback\n6.Exit\n")
    while(True):
        ch = int(input("Enter your choice:\n"))
        if(ch==1):
            #Update customer where cid(sql)= scid
            phno=int(input("Enter new phone no:"))
            addr=input("Enter new address:")
            c.execute("update cust_ph set cphno='%d' where cid='%d'",phno,scid)
            c.execute("update cust_addr set address='%s' where cid='%d'",addr,scid)
            c.execute("commit")
            break
        elif(ch==2):
            #select from food_menu
            c.execute("select * from fmenu")
            for line in c:
                print(line)
            c.execute("commit")
            break
        elif(ch==3):
            mc = int(input("Enter menu code of the food item:"))
            cart(scid,mc)
            break
        elif(ch==4):
            #select from food_menu where....
            f=input("You can do filtered search based on veg/non-veg....\n")
            c.execute("select * from fmenu where cat='%s'",f)
            for line in c:
                print(line)
            break
        elif(ch==5):
            cf = input("Enter caterer feedback:")
            df = input("Enter delivery feedback:")
            db_id = int(input("Enter delivery boy id:"))
            deli_id = int(input("Enter delivery id:"))
            ord_id = int(input("Enter order id:"))
            #insert into order_placed cf = caterer_f df = delivery_f db_id =dboy_id deli_id =del_id ord_id = order_id 
            c.execute("insert into order('%s','%s','%d','%d','%d')",cf,df,db_id,deli_id,ord_id)
            c.execute("commit")
            break
        elif(ch==6):
            print("Quitting......\n")
            exit(0)
        else:
            ch=0
            print("Wrong choice........Try again....\n")

def ven():
    ch=0
    #login
    name = input("Username:")
    venid = int(input("Enter id:"))
    c.execute("select vname from vendor where vid='%s' and vname='%s'",venid,name)
    svid=c.fetchone()
    print(svid)
    print("What do you want to do?....\n")
    print("1.Add in menu\n2.Delete from menu\n3.Update in menu\n4.Edit details\n5.Exit\n")
    while(True):
        ch = int(input("Enter your choice:\n"))
        if(ch==1):
            fname=input("Enter food item name:")
            categ=input("Enter category- veg or non-veg(v/n):")
            rem=input("Enter remarks(spicy/extra cheesy...):")
            mc=assign()
            #insert in fmenu
            #assign mc=mcode
            c.execute("insert into fmenu values('%d','%s','%s','%s')",mc,fname,categ,rem)
            c.execute("commit")
            break
        elif(ch==2):
            item = input("Enter item to delete:")
            #select from fmenu where .....
            c.execute("select * from fmenu join catered_by on fmenu.mcode=catered_by.mcode where fmenu.item_name='%s'",item)
            for line in c:
                print(line)
            mcod=int(input("Enter menu code:"))
            c.execute("delete from fmenu where mcode='%d'",mcod)
            c.execute("delete from catered_by where mcode='%d'",mcod)
            c.execute("commit")
            break
        elif(ch==3):
            remark = input("Enter food remarks:")
            c.execute("select * from fmenu join catered_by where catered_by.vid='%d'",svid)
            for line in c:
                print(line)
            mcod=int(input("Enter menu code:"))
            c.execute("update fmenu set remarks='%s' where mcode='%d'",remark,mcod)
            c.execute("commit")
            #update in  fmenu remarks = remark where ....
            break
        elif(ch==4):
            r = int(input("Enter your new rating:"))
            salr = int(input("Enter your new income:"))
            phno=int(input("Enter new phone no:"))
            #update in vendor rating= r and income=salr
            c.execute("update vendor set rating='%d',income='%d' where vid='%d'",r,salr,svid)
            c.execute("update vendor_ph set vphno='%d' where vid='%d'",phno,svid)
            c.execute("commit")
            break
        elif(ch==5):
            print("Quitting......\n")
            exit(0)
        else:
            ch=0
            print("Wrong choice........Try again....\n")

def db():
    ch=0
    #login
    name = input("Username:")
    did = int(input("Enter id:"))
    c.execute("select dboy_id from dboy where dboy_id='%d' and dname='%s'",did,name)
    sdid=c.fetchone()
    print(sdid)
    print("What do you want to do?....\n")
    print("1.Edit details\n2.View orders\n3.Exit\n")
    while(True):
        ch = int(input("Enter your choice:\n"))
        if(ch==1):
            addr = input("Enter your new address:")
            salr = int(input("Enter your new salary:"))
            #update in dboy address = addr and sal=salr
            c.execute("update dboy set address='%s',sal='%d' where dboy_id='%d'",addr,salr,sdid)
            c.execute("commit")
            break  
        elif(ch==2):
            #select from orders where dboy_id=sdid
            c.execute("select * from orders where dboy_id='%d'",sdid)
            for line in c:
                print(line)
            break
        elif(ch==3):
            print("Quitting......\n")
            exit(0)
        else:
            ch=0
            print("Wrong choice........Try again....\n")
    

print(".............................................Welcome................................................\n");
ch=0
print("What do you identify yourself as?....\n")
print("1.Customer\n2.Vendor\n3.Delivery boy\n4.Exit\n")
while(True):
    ch = int(input("Enter your choice:\n"))
    if(ch==1):
        cust()
        break
    elif(ch==2):
        ven()
        break
    elif(ch==3):
        db()
        break
    elif(ch==4):
        print("Quitting......\n")
        exit(0)
    else:
        ch=0
        print("Wrong choice........Try again....\n")











