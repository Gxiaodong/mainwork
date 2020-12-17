import numpy as np


class Prediction:


    def __init__(self,vec_dict,all_dict):
        self.vec_dict=vec_dict
        self.all_dict=all_dict

    def cos_sim(self, vector_a, vector_b):
        """
        计算两个向量之间的余弦相似度
        :param vector_a: 向量 a
        :param vector_b: 向量 b
        :return: sim
        """
        vector_a = np.mat(vector_a)
        vector_b = np.mat(vector_b)
        num = float(vector_a * vector_b.T)
        denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        cos = num / denom
        sim = 0.5 + 0.5 * cos
        return sim

    # 通过序号反查name  输入的a是字符串
    def get_english_name(self,a):
        english_list = list(filter(lambda x: self.all_dict.get(x) == a, self.all_dict.keys()))
        return english_list

    def get_number_of_name(self,name):
        return self.all_dict[name]

    def get_top3_sim_exp(self, new_name):
        numberlist=['','','']
        top3list=[0,0,0]

        new_vec=self.vec_dict[self.get_number_of_name(new_name)]

        for number, vec in self.vec_dict.items():
            sim = self.cos_sim(new_vec, vec)
            if  sim!=1:
                numberlist,top3list=self.top3_list(sim,number,top3list,numberlist)


        return numberlist,top3list

    def top3_list(self,sim,number,top3list,numberlist):
        if sim>=top3list[0]:
            top3list[2]=top3list[1]
            top3list[1] = top3list[0]
            top3list[0] = sim
            numberlist[2] = numberlist[1]
            numberlist[1] = numberlist[0]
            numberlist[0] = number
        elif sim>=top3list[1] and sim<top3list[0]:
            top3list[2] = top3list[1]
            top3list[1] = sim
            numberlist[2] = numberlist[1]
            numberlist[1] = number
        elif sim>=top3list[2] and sim<top3list[1]:
            top3list[2] = sim
            numberlist[2] = number
        else:
            pass
        return numberlist,top3list

    def get_trans_sim_exp(self, new_name):
        numberlist=['','','']
        top3list=[0,0,0]

        new_vec=self.all_dict[new_name]

        for name, vec in self.all_dict.items():
            sim = self.cos_sim(new_vec, vec)
            if  sim!=1:
                numberlist,top3list=self.get_trans_veclist(sim,name,top3list,numberlist)
        return numberlist,top3list


    def get_trans_veclist(self,sim,number,top3list,numberlist):
        if sim>=top3list[0]:
            top3list[2]=top3list[1]
            top3list[1] = top3list[0]
            top3list[0] = sim
            numberlist[2] = numberlist[1]
            numberlist[1] = numberlist[0]
            numberlist[0] = number
        elif sim>=top3list[1] and sim<top3list[0]:
            top3list[2] = top3list[1]
            top3list[1] = sim
            numberlist[2] = numberlist[1]
            numberlist[1] = number
        elif sim>=top3list[2] and sim<top3list[1]:
            top3list[2] = sim
            numberlist[2] = number
        else:
            pass
        return numberlist,top3list




def main():
    vec_dict = {}
    fopen = open("data/math.emmbeddings")
    for line in fopen.readlines():
        line = str(line).replace("\n", "")  # 注意，必须是双引号，找了大半个小时，发现是这个问题。。
        a=line.split(' ')
        a_float=[]
        for i in  a:
            a_float.append(float(i))
        vec_dict[a[0]] = a_float[1:]
        # split（）函数用法，逗号前面是以什么来分割，后面是分割成n+1个部分，且以数组形式从0开始
    fopen.close()

    entity_dict = np.load('data/entitis.npy').item()
    relation_dict = np.load('data/relations.npy').item()
    all_dict = dict(entity_dict, **relation_dict)


    pre = Prediction(vec_dict, all_dict)

    node = "Segment"
    names,vecs = pre.get_top3_sim_exp(node)
    print("输入词：%s"%node)
    for i in names:
        print("输出匹配前三位近似词：%s" % pre.get_english_name(i))

    # vec_dict = {}
    # entity_dict = {}
    # relation_dict = {}
    # f1open = open("data/entityVector.txt")
    # for line in f1open.readlines():
    #     line = str(line).replace("\n", "").replace("[","").replace("]","").replace(",","")  # 注意，必须是双引号，找了大半个小时，发现是这个问题。。
    #     a = line.split('\t')
    #     b = a[1].split(" ")
    #     a_float = []
    #     for i in b:
    #         a_float.append(float(i))
    #
    #     entity_dict[a[0]] = a_float
    #     # split（）函数用法，逗号前面是以什么来分割，后面是分割成n+1个部分，且以数组形式从0开始
    # f1open.close()
    # f2open = open("data/relationVector.txt")
    # for line in f2open.readlines():
    #     line = str(line).replace("\n", "").replace("[", "").replace("]", "").replace(",","")  # 注意，必须是双引号，找了大半个小时，发现是这个问题。。
    #     a = line.split('\t')
    #     b = a[1].split(" ")
    #     a_float = []
    #     for i in b:
    #         a_float.append(float(i))
    #
    #     entity_dict[a[0]] = a_float
    #     # split（）函数用法，逗号前面是以什么来分割，后面是分割成n+1个部分，且以数组形式从0开始
    # f2open.close()
    #
    # all_dict = dict(entity_dict, **relation_dict)
    #
    # pre = Prediction(vec_dict, all_dict)
    #
    # node = "StraightLine"
    # names,vecs = pre.get_trans_sim_exp(node)
    # print("输入词：%s", node)
    # for i in range(3):
    #     print("输出匹配前三位近似词：%s " % names[i])










if __name__ == '__main__':
    main()






