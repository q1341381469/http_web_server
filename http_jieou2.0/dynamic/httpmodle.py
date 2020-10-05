from pymysql  import connect 
import re


url_dict = dict()


def route(name):
    def start_fun(fun):
        
        def call_fun():
              fun()
        url_dict[name] = fun
        return call_fun
    return start_fun    




@route('/index.html')
def index():

    with open(r'./templates/index.html','r',encoding='utf-8') as f:
         f = f.read()

     # 创建Connection连接
    conn = connect(host='localhost',port=3306,database='stock_db',user='root',password='hlgjiayou666',charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()
    hhh=""

    content = """

                 <tr>
                <td>%d</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>
                    <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
                </td>
                </tr>

     """
    cs.execute('select * from info;')


    text = cs.fetchall()
    for i  in  text:
         hhh += content %(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[1])
    cs.close()
    conn.close()
    
       
    f = re.sub( r"\{%content%\}",hhh , f)

    return  f
@route('/center.html')
def center():

    conn = connect(host='localhost',port=3306,database='stock_db',user='root',password='hlgjiayou666',charset='utf8')
    # 获得Cursor对象
    cs = conn.cursor()

    with open(r'./templates/center.html','r',encoding='utf-8') as f:

        f = f.read()

    hhh=""

    content = """

                     <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>
                    <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                </td>
                <td>
                    <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
                </td>
            </tr>

     """
    cs.execute('select i.code, i.short ,i.chg ,i.turnover,i.price,i.highs ,f.note_info from  info as i   inner  join   focus as f on i.id = f.info_id;')


    text = cs.fetchall()
    for i  in  text:
         hhh += content %(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[0],i[0])
    cs.close()
    conn.close()
    
       
    f = re.sub( r"\{%content%\}",hhh , f)

    return  f
        
 
        # re.sub( {%content%},connent , f)

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    file_path = environ['file_path']

    # if file_path == '/index.py':
    #     return  index()
    # elif file_path =='/center.py':
    #     return center()


    # else:

    #   return  '哈哈哈哈'
    try:
        a =  url_dict[file_path]
        return  a()
    except Exception as ret:
        return '%s'%ret