from app import app,db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash


class User(UserMixin):

    meta={
        "collection":"user",
        "ordering":["-id"],
        "strict":True
    }

    def __init__(self, user_data):
        self.id = user_data[0][0]
        self.firstname = user_data[0][1]
        self.lastname = user_data[0][2]
        self.username = user_data[0][3]
        self.GM = user_data[0][4]
        self.password_hash = user_data[0][5]

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


MAIN_TYPE_NAME = {'行政效能': 0, '宣传舆论': 1, '医政监管': 2, '人口计生': 3, '教育体制':4, '教育行政管理':5, '文化':6,
                  '人力资源':7, '社会组织':8, '福利慈善':9,'市容城管':10,'物业服务管理监督':11,'社区公共管理':12,
                  '住宅区（园区）或建筑物内安全、环卫问题':13, '民间纠纷':14,'经济违法行为举报':15,
                  '经济纠纷':16, '警务督察':17,'户籍证件':18, '工业噪声':19, '建筑施工噪声':20, '商业经营噪声':21,
                  '营业性文化娱乐噪声':22, '交通运输噪声':23, '社会生活噪声':24, '禽畜养殖污染':25,
                  '工业、住宅废气扰民':26, '服务行业废气扰民':27, '水污染':28, '扬尘污染':29, '固体废物':30,
                  '生态破坏':31, '跨河桥、河堤、河道破损':32, '供、排水及水质问题':33, '土地资源管理':34,
                  '违法建筑与用地行为':35, '城乡规划':36, '住房保障和房地产':37, '垃圾问题':38, '渣土问题':39,
                  '道路保洁':40, '公共设施保洁':41, '绿化养护':42, '废弃物堆放':43, '占道经营':44, '车辆乱停放':45,
                  '安全生产':46, '宣传广告违法行为':47, '其他市容违法行为或影响市容事件':48, '环卫设施设置及维护':49,
                  '交通设施':50, '道路设施':51, '公用部件':52, '市政、公共设施设置及维护':53, '城市公共资源管理':54,
                  '道路规划建设':55, '公共交通管理':56, '消防设施安全':57, '线路消防安全':58,'燃气安全':59,
                  '危险化学品安全':60, '道路交通安全':61, '劳动就业':62, '劳动社保':63, '食品安全':64, '无证无照经营':65,
                  '价格监管':66, '建设工程质量':67, '互联网与通讯':68, '地质安全':69, '消费维权':70, '食药监问题':71,
                  '体育':72, '医疗机构违规经营':73, '面源污染隐患':74, '医患纠纷':75, '公共卫生':76,
                  '招生中的违法行为':77, '工商经济联络':78, '双拥优抚':79, '社会救助':80, '小散乱污':81,
                  '其他公共安全隐患':82, '教师队伍和待遇':83, '教育收费':84,'招录辞退':85, '党的建设':86,'社会治安':87,
                  '经济管理':88, '表达情感':89, '集体土地上房屋拆迁与补偿':90, '城市建设和市政管理':91,

                  '人口房屋':92,
                  '交通管理':93, '普法教育':94, '刑案侦破':95, '危险废物、化学品污染':96, '核安全':97, '环保标志管理':98,
                  '征转地审批': 99, '房屋征收':100, '建筑市场':101, '建筑设计':102, '建筑安装':103, '更改房屋结构':104,
                  '网约车管理':105, '建筑消防安全':106, '劳动保护': 107, '校园安全': 108, '药品（医疗器械）监管': 109,
                  '商标管理': 110, '市场垄断': 111, '知识产权': 112, '文化市场违法行为':113, '卫生问题':114,
                  '旅游市场管理': 115, '综合事件采集':116, '医疗机构违规收费': 117, '义工联':118, '工作纪律':119,
                  '违反计生政策':120, '出入境检验检疫':121, '社区建设':122, '教学违规':123,'复退安置':124,'编制职务':125,
                  '军转安置':126, '野生资源管理':127,'宣传教育':128,'环保管理':129,'国有土地上房屋征收与补偿':130,
                  '科学技术':131, '信息化建设':132, '质监检验检疫':133
}

STREET_NAME = {"龙田街道": 0, "坪山街道": 1, "碧岭街道": 2, "坑梓街道": 3, "马峦街道": 4, "石井街道": 5}


EVENT_PROPERTY_NAME = {"投诉": 0, "咨询": 1, "感谢": 2, "建议": 3, "求决": 4, "其他": 5}


EVENT_TYPE_NAME = {'安全隐患': 0,'党纪政纪':1,'党建群团':2,'规土城建':3,'环保水务':4,'交通运输':5,'教育卫生':6,
                   '劳动社保':7,'民政服务':8,'社区管理':9,'食药市监':10,'市容环卫':11,'市政设施':12,'统一战线':13,
                   '文体旅游':14,'治安维稳':15,'专业事件采集':16,'组织人事':17}

COMMUNITY_NAME = { '老坑社区':0,'六和社区':1,'沙湖社区':2,'六联社区':3,'金沙社区':4,'秀新社区':5,'坑梓社区':6,
                   '坪环社区':7,'和平社区':8,'坪山社区':9,'龙田社区':10,'沙田社区':11,'石井社区':12,'南布社区':13,
                   '沙坣社区':14,'金龟社区':15,'江岭社区':16,'碧岭社区':17,'竹坑社区':18,'汤坑社区':19,'田头社区':20,
                   '田心社区':21,'马峦社区':22}
