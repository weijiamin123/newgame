# 历史小游戏
import random
class HistoryGame:
    def __init__(self):
        self.total_scores = 0  # 历史游戏自身的总分
    def show(self):
        print('本游戏兼具历史,趣味以及八卦野史,请自行分辨!')
        print("欢迎进入游戏！")

    def zhanguo_history(self):
        zhanguo_scores = 0
        input("请按任意键继续")
        print("""在赵国做质子的异人(后来的秦庄襄王)在邯郸接受了
              吕不韦献上的女子赵姬,后来赵姬生下嬴政,即后来的始
              皇帝.据野史记载,赵姬在认识异人之前已经怀有身孕,
              其实是吕不韦才是嬴政的老爹,你认为这是真的吗?""")
        print("1-是真的")
        print("2-假的")
        player_choice1 = input("请输入数字:")
        if player_choice1 == '1':
            print('无鸡之谈,把你烧成兵马俑下去陪始皇帝')
        else:
            zhanguo_scores += 1
            print('尔乃朕之心腹,赐汝名赵高')
        input("请按任意键继续")
        print("""秦将白起号称杀神,请问是他灭了赵国吗?""")
        print("1-是真的")
        print("2-假的")
        player_choice2 = input("请输入数字:")
        if player_choice2 == '1':
            print('白起被秦昭襄王(嬴政他曾祖父)刺剑自裁,历史上是王翦灭的赵国,白起这个人压根就熬不到嬴政当皇帝')
        else:
            zhanguo_scores += 1
            print('不错,你的历史tips还算可以')
        input("请按任意键继续")
        print("""相关始皇帝即位后,民间常有"楚虽三户,亡秦必楚"说法,请问项羽他爸是谁?""")
        print("1-项梁")
        print("2-项伯")
        print("3-项少龙")
        player_choice3 = input("请输入数字:")
        if player_choice3 == '3':
            print('少看点穿越剧,古天乐也只是一个相貌平平无奇的人,扣1分')
            zhanguo_scores -= 1
        else:
            zhanguo_scores += 1
            print('史料无记载,壮士如此勇猛,却不知他爹是谁?肯定有内幕.送1分')
        input("请按任意键继续")
        print("""以下哪个战役发生在战国时期?""")
        print("1-巨鹿之战")
        print("2-垓下之战")
        print("3-桂陵之战")
        print("4-暗渡陈仓")
        player_choice4 = input("请输入数字:")
        if player_choice4 == '3':
            print('恭喜答对了\n兵家亚圣孙膑复仇庞涓之战,纵横派鬼谷门人的一直纷争不断,包括后来的剑圣盖聂和流沙卫庄,不死不休')
            zhanguo_scores += 1
        else:
            print('自己查去吧,不要游戏制作人.')
        print(f'以上问题你总共的了{zhanguo_scores}分')
        if zhanguo_scores >= 4:
            print('good,优秀')
        if 3 <= zhanguo_scores < 4:
            print('一般般')
        else:
            print('糟糕,快回去问小学生')
        return zhanguo_scores

    def han_history(self):
        han_scores = 0
        print("""楚汉争霸,成语背水一战是指的是谁?""")
        print("1-项羽")
        print("2-韩信")
        print("3-刘邦")
        print("4-周勃")
        player_choice1 = input("请输入数字:")
        if player_choice1 == '2':
            print('恭喜你答对了!\n韩信,号称兵仙,多个成语都出自他,狡兔死\走狗烹,成也萧何败也萧何,被吕雉设计杀害.')
            han_scores += 1
        else:
            print('答错了,虽然这几位也很厉害')
        input("请按任意键继续")
        print("汉武帝前期,朝局受窦太后等外戚把持,但他抽到了SSD的武将,封狼居胥\饮马瀚海是中国古代武将的最高荣誉,汉武时期做到这一点的人是谁?")
        print("1-李广")
        print("2-卫青")
        print("3-霍去病")
        print("4-周亚夫")
        player_choice2 = input("请输入数字:")
        if player_choice2 == '3':
            print('恭喜答对了!')
            print('''霍去病-17岁随卫青出征，率八百骑兵奇袭匈奴大营，封 “冠军侯”；
            河西之战大破匈奴，收复河西走廊，设酒泉、武威等四郡；漠北之战 “封狼居胥”，
            直达瀚海（今贝加尔湖）可惜,英年早逝（24 岁）,他所完成的成就在古代无人能出其右!''')
            han_scores += 1
        else:
            print('答错了,没有第二次机会给你')
        input("请按任意键继续")

        print("""汉武帝晚年,受蒙蔽,巫蛊之乱,刺死太子\皇后卫子夫,
            历年的征讨匈奴,挥霍了文景两朝屯下的基业,造成王朝内部经济凋敝.
            西汉后期,外戚逐渐把持朝政,公元 8 年，王莽声称得到 “天命” 授权，
            逼迫孺子婴禅位，改国号为 “新”，定都长安，史称 “新莽”，西汉正式灭亡。
            """)
        print("""据传,由于王莽实行的新政的意识过于超前,怀疑他是穿越回去的人,
            但是新政并不符合当时的情况,导致全国大规模农民起义,公元 25 年，刘秀
            （汉景帝后裔）平定战乱，称帝建立东汉，恢复汉朝统治。""")
        input("请按任意键继续")
        print('请问灭亡东汉的是哪个?')
        print("1-曹操")
        print("2-曹丕")
        print("3-司马懿")
        print("4-司马昭")
        player_choice3 = input("请输入数字:")
        if player_choice3 == '2':
            print('老子没做的事,儿子做了,"煮豆燃豆豉,豆在斧中泣,本事童根生,相煎何太急"')
            han_scores += 1
        if player_choice3 == '1':
            print(f"一生未称帝,挟天子以令诸侯.爱好是别人的老婆\"铜雀春深锁二乔\",写诗\"青青子衿悠悠我心,但为君故沉吟至今\",吾等楷模")
            print('虽然答错了.但送1分')
            han_scores += 1
        else:
            print('司马家,历史之耻.扣1分')
            han_scores -= 1
        input("请按任意键继续")
        print("蜀汉算汉朝吗?")
        print("1-算")
        print("2-不算")
        player_choice4 = input("请输入数字:")
        if player_choice4 == '1':
            print('''史书称刘备汉景帝之子中山靖王刘胜后裔,其实就是个卖草鞋的,
                但是如果蜀汉能够灭吴魏,再造一统,那另外说,影响深远.''')
        else:
            print('确实不算,自关羽被吕蒙偷家之后,失去荆州,已经偏离诸葛亮最初的战略部署,三国中基本蜀汉排老末.')
            print('加一分.')
            han_scores += 1
        input("请按任意键继续")
        print(f'以上汉朝代的问题你总共的了{han_scores}分')
        if han_scores >= 4:
            print('good,优秀')
        if 3 <= han_scores < 4:
            print('一般般')
        else:
            print('糟糕,快回去问小学生')
        return han_scores

    def tang_history(self):
        tang_scores = 0
        print("天策上将指的是谁?")
        print("1-秦叔宝")
        print("2-尉迟恭")
        print("3-李世民")
        print("4-李靖")
        player_choice1 = input("请输入数字:")
        if player_choice1 == '3':
            print('恭喜你答对了!天策上将,封无可封.功劳太大,李渊除非给皇帝的位置给他坐')
            tang_scores += 1
        else:
            print('答错了,虽然这几位也很厉害,李靖-唐朝初期的战神,秦叔宝,尉迟恭-门神')
        input("请按任意键继续")
        print("以下谁未帮助李世民参与玄武门之变?")
        print("1-长孙无忌")
        print("2-魏征")
        print("3-秦叔宝")
        print("4-程咬金")
        player_choice2 = input("请输入数字:")
        if player_choice2 == '2':
            print('恭喜答对了!')
            print('''他是太子李建成的心腹!多次跟李建成说先下手,后
                来李建成,李元吉在玄武门被杀后,被李世民收服,要么是李世民
                魅力大,但是也有一种可能是李建成的势力太大,如果见到心腹都
                能被重用,稳住其他人不搞事,徐徐图之.!''')
            tang_scores += 1
        else:
            print('答错了,没有第二次机会给你')
        input("请按任意键继续")

        print("李白\杜甫\高适大器晚成的是谁?")

        print("1-李白")
        print("2-杜甫")
        print("3-高适")
        print("4-白居易")
        player_choice3 = input("请输入数字:")
        if player_choice3 == '3':
            print('恭喜答对了!\n高适在安史之乱爆发后,从52岁才开始转命,执掌一方节度使.边塞诗人."莫愁前路无知己，天下谁人不识君。"')
            tang_scores += 1
        elif player_choice3 == '2':
            print(f"青年的杜甫李白头号迷弟,一生经历了盛唐\安史之乱,老年过得比较凄凉.\"南村群童欺我老无力,公然抱茅入竹去\"")
        elif player_choice3 == '1':
            print("青年的杜甫李白头号迷弟,一生经历了盛唐\安史之乱,老年过得比较凄\"南村群童欺我老无力,公然抱茅入竹去\"")
        else:
            print('打错了')
        pass_1 = input("请按任意键继续")
        print("中国古代唯一的以为女皇帝是谁?")
        print("1-吕雉")
        print("2-武则天")
        print("3-慈禧")
        player_choice4 = input("请输入数字:")
        if player_choice4 == '2':
            print('恭喜答对了!')
            print('''武则天:心机woman,被唐太宗宠信过,后来唐太宗死了,儿子继承黄位的同时,
                也继承了这个n妈(不太懂武则天排行老几),由于是心机woman,能力又强,在唐高宗
                李治的时候就可以与李治一同上朝处理国事,也叫作二圣临朝,后来李治也挂了,
                先废了几个儿子(中宗李显、睿宗李旦),公元690年,快70岁的武则天称帝,改国号'周'.
                说明了大家要苟得住,可能到我们这代的时候要75岁才能退休.''')
            tang_scores += 1
        else:
            print('答错了,可能这位才对你胃口.')
            print('扣一分.')
            tang_scores -= 1
        input("请按任意键继续")
        print(f'以上唐朝代的问题你总共的了{tang_scores}分')
        if tang_scores >= 3:
            print('good,优秀')
        else:
            print('糟糕,快回去问小学生')
        return tang_scores

    def start(self):

        self.show()

        print('从战国开始')
        zhan_score = self.zhanguo_history()
        self.total_scores += zhan_score
        print(f'你目前已经总得分为{self.total_scores}')

        input("请按任意键继续汉代的问答")
        han_score = self.han_history()
        self.total_scores += han_score
        print(f'你目前已经总得分为{self.total_scores}')

        input("请按任意键继续汉代的问答")
        tang_score = self.tang_history()
        self.total_scores += tang_score
        print(f'你目前已经总得分为{self.total_scores}')

        print(f'\n🎉 【历史小游戏】结束！你的最终得分为：{self.total_scores}')

class Game_21:
    def game_show(self):

        print('游戏名称：要管三七二十一（抢21）')
        print('游戏作者: 木木(姜杰)')
        print('一个人可以走的很快，但是一群人可以走的更远！\n欢迎来到沃林游戏联盟!!!')
        print('*'*6)
        print('*'*6)
        print('游戏规则:你可以输入一个初始值"1"或者"2",\n'
              '接下来，木木和你只能在之后数值的基础上增加"1"或者"2",\n'
              '直到谁先抢到21为止，抢到21获胜。')
        print('*'*6)
        print('游戏开始咯~~~',end='')

    def game_start(self):

        self.user=int(input('请报出你的数字：'))
        print('游戏名称：独孤求败之勇夺二十一')
        print('游戏作者: 独孤木(姜杰)')
        print('欢迎来到华山之巅挑战者独孤木!!!')
        print('*'*6)
        print('*'*6)
        print('游戏规则:你可以输入一个初始值"1"或者"2",\n'
              '接下来，独孤木和你只能在之后数值的基础上增加"1"或者"2",\n'
              '直到谁先抢到21为止，抢到21获胜。')
        print('*'*6)
        print('游戏开始咯~~~',end='')

        self.user=int(input('请报出你的数字：'))
        while True:
            if self.user == 1 or self.user == 2:
                com=self.user+(3-self.user)
                print(f'独孤木输出{com}')
                while 1:
                    if self.user==19 or self.user==20:
                        print('独孤木勇夺21')
                        print('此战结束***你退下吧\n下一位***')
                        break
                    elif com==19 or com==20:
                        print('好了,可以了，你踩到狗屎了！\n木木不和你计较\n游戏结束***')
                        break
                    elif com>10:
                        self.user = int(input('注意注意！！！，快到21了\n请思考一下，再报出你的数字：'))
                        while True:
                            if self.user-com == 1 or self.user-com == 2:
                                com = self.user+(3+com-self.user)
                                break
                            else:
                                self.user = int(input('都快到21了，你还在这给独孤木乱整是吧！！！\n'
                                                 f'独孤木输出的是" {com} "给你个机会再输入一次：'))
                        print(f'独孤木知道自己要赢了，闭着眼睛出：{com}')
                    else:
                        user = int(input('请再报出你的数字：'))
                        while True:
                            if self.user-com==1 or self.user-com==2:
                                break
                            else:
                                self.user = int(input('说了别乱整！！！，看清规则，你的输出只能在木木输出的基础上增加"1"或者"2"，\n'
                                                 f'独孤木输出的是" {com} "给你个机会再输入一次：'))
                        com = self.user+(3+com-self.user)
                        print(f'独孤木随意的输出：{com}')
                break
            else:
                self.user = int(input('别乱整！，看清规则，你只能输入"1"或者"2"，\n给你个机会再输入一次：'))

class Game_chen:
    import random
    def game_chen(self):

        print('游戏名称：密码破译游戏')
        print('游戏作者：陈宝如')
        print('''游戏规则：系统自动生成一个4位数字密码（1-9)不重复，你需要每次提交一个4位数候选密码，规则同密码一样，与系统对比，系统对比后给出反馈;
        "A":数字正确且位置正确（如真实密码1582，候选1673，"1"匹配，记1A）
        "B":数字正确但位置错误（如真实密码1582，候选2534，"5"记1A，"2"记1B，反馈"1A1B")
        在8次内成功破译密码则赢，没有破译出则输了。''')

    def game_chenstart(self):

        password_numbers=self.random.sample(range(1,10),4)
        password=''.join([str(num) for num in password_numbers])
        i = 0
        while True:
            b = []
            s=[]
            i += 1
            print(f'这是第{i}次猜测')
            found =True
            self.guess_word = input('请输入你猜想的密码（输入Q/q退出游戏）：').replace(' ','')
            if self.guess_word.upper() == 'Q':
                print('已退出')
                return False
            for j in self.guess_word:
                if s.count(j) ==0:
                    s.append(j)
                    if password[0] ==j :
                        if self.guess_word.index(j) == 0:
                            b.append('1A')
                        else:
                            b.append('1B')
                    elif password[1] ==j:
                        if self.guess_word.index(j) == 1:
                            b.append('1A')
                        else:
                            b.append('1B')
                    elif password[2] ==j:
                        if self.guess_word.index(j) == 2:
                            b.append('1A')
                        else:
                            b.append('1B')
                    elif password[3] ==j:
                        if self.guess_word.index(j) == 3:
                            b.append('1A')
                        else:
                            b.append('1B')
                else:
                    found=False
                    print('你输入的密码格式有误，请重新输入')
                    break
            if not found:
                continue
            if i >=8:
                print(f'游戏结束，你输了,正确密码是{password}')
                break
            if ''.join(b) == '1A1A1A1A':
                print('你赢了，游戏结束')
                return True
            else:
                print(f'密码猜测错误，反馈为:{"".join(b)}')

class Down_city:

    player_health = {
        'hp': 100,
        'mp': 100,
        'attack': 20,
    }

    def dice(self):  # 返回骰子3次的点数和

        dice_num = 0
        for i in range(3):
            dice_num += random.randint(1, 6)
        return dice_num


    def attack(self):
        self.attack_in = input('你将要发起攻击，请确认-Y')
        if self.attack_in.upper() == 'Y':
            attack_num = self.dice()
            if attack_num >= 3:
                print(f"点数为{attack_num}，判定有效，攻击成功")
                return (1, attack_num)
            else:
                print(f"点数为{attack_num}，判定无效，攻击失败")
                return (0, 0)
        print("你取消了攻击")
        return (0, 0)

    def skill(self):
        self.skill_in = input('你将要发起技能，请确认-Y')
        if self.skill_in.upper() == 'Y':
            if  self.player_health['mp'] >= 10:
                skill_num =  self.dice()
                if skill_num >= 12:
                    print(f"点数为{skill_num}，判定有效，技能成功")
                    return (1, 0)
                else:
                    print(f"点数为{skill_num}，判定无效，技能失败")
                    return (0, 0)
            else:
                print("你的MP不足，无法施放技能！")
                return (0, 0)
        print("你取消了技能")
        return (0, 0)

    def run(self):
        self.run_in = input('你将要发起逃跑，请确认-Y')
        if self.run_in.strip().upper() == 'Y':
            run_num = self.dice()
            if run_num >= 9:
                print(f"点数为{run_num}，判定有效，逃跑成功")
                return (1, 0)
            else:
                print(f"点数为{run_num}，判定无效，逃跑失败")
                return (0, 0)
        print("你取消了逃跑")
        return (0, 0)

    def monster_attack(self):
        monster_attack1 =  self.dice()
        if monster_attack1 > 8:
            monster_attack2 = 1+ monster_attack1 / 21
            return (1, monster_attack2)
        else:
            return (0, 0)


    # ----------------------
    #       修复后的战斗
    # ----------------------
    def fight(self,monster_health):
        while True:
            print(f"\n怪物HP：{monster_health['hp']}")
            print(f"你的HP：{self.player_health['hp']}  MP：{self.player_health['mp']}")
            print("遭遇怪物")

            while True:
                try:
                    self.fight_choice = int(input('选择你的手段\n1---攻击\n2---技能\n3---逃跑\n'))
                    if self.fight_choice in [1, 2, 3]:
                        break
                    else:
                        print("请输入1-3之间的数字！")
                except ValueError:
                    print("输入错误，请输入数字1-3！")

            # ---- 玩家攻击 ----
            if self.fight_choice == 1:
                fight_attack =  self.attack()
                attack_num = fight_attack[1]
                if fight_attack[0] == 1:
                    damage = self.player_health['attack'] * (1 + attack_num / 100)
                    monster_health['hp'] -= damage
                    print(f"你成功造成伤害 {damage:.2f}")
                else:
                    print("你没有造成伤害")

            # ---- 玩家技能 ----
            elif self.fight_choice == 2:
                fight_skill = self.skill()
                if fight_skill[0] == 1:
                    monster_health['hp'] -= 40
                    self.player_health['hp'] += 40
                    self.player_health['mp'] -= 10
                    print("你放出了技能！造成40伤害，回复40HP")
                else:
                    print("技能失败")

            # ---- 玩家逃跑 ----
            elif self.fight_choice == 3:
                fight_run = self.run()
                if fight_run[0] == 1:
                    print("你成功逃跑了！")
                    return "run"
                else:
                    print("逃跑失败！")

            # ---- 怪物死亡判断 ----
            if monster_health['hp'] <= 0:
                print("怪物倒下了！")
                return "win"

            # -------------------------
            #  怪物攻击（只有怪物活着才攻击）
            # -------------------------
            print("怪物即将发起攻击")
            m = self.monster_attack()

            if m[0] == 1:
                damage = monster_health['attack'] * (1 + m[1] / 100)
                self.player_health['hp'] -= damage
                print(f"怪物攻击成功！你受到 {damage:.2f} 点伤害")
            else:
                print("怪物攻击落空")

            # ---- 玩家死亡判断 ----
            if self.player_health['hp'] <= 0:
                print("你死了！")
                return "lose"


    # ----------------------
    #       主循环
    # ----------------------
    def down_city(self):

        while True:
            game = input('欢迎来到地下城，开始你的冒险吧\n1.开始游戏\n2.帮助\n3.退出\n')

            if game == '1':
                self.player_health = {'hp': 100, 'mp': 100, 'attack': 35}

                print('你在地下城门口醒来，里面传出嘶嘶叫声')

                while True:
                    enter = input('是否进入下一层？\n1-进入\n2-退出\n')

                    if enter == '1':
                        monster_health = {'hp': 60, 'attack': 20, 'defense': 10}
                        self.player_health['mp'] += 1

                        result =self.fight(monster_health)

                        if result == "win":
                            print("你通关这一层！准备下一层……")
                            continue
                        elif result == "lose":
                            print("你失败了……回到地城入口")
                            break
                        elif result == "run":
                            print("你逃回来了……")
                            continue

                    elif enter == '2':
                        break

            elif game == '2':
                print("这是一个基于骰子判定的地下城冒险……（省略帮助说明）")

            elif game == '3':
                confirm = input("确定退出？ 1-退出 2-返回\n")
                if confirm == '1':
                    break


def game_menu():

    print("=" * 30)
    print("1. 野史冲浪")
    print("2. 必输21点")
    print("3. 绝密2025")
    print("4. 地下城勇士")
    print("5. 退出游戏")
    print("=" * 30)

    while True:
        choice = input("请输入你要选择的游戏编号（1/2/3/4/5）：")
        if choice == "1":
            # 实例化历史游戏并启动
            game1 = HistoryGame()
            game1.start()

        elif choice == "2":
            # 实例化游戏并启动
            game2 = Game_21()
            game2.game_show()
            game2.game_start()

        elif choice == "3":
            # 实例化游戏并启动
            game3 = Game_chen()
            game3.game_chen()
            game3.game_chenstart()

        elif choice == "4":
            # 实例化游戏并启动
            game4 = Down_city()
            game4.down_city()

        elif choice == "5":
            break

        else:
            print("输入错误，请重新选择！")



if __name__ == "__main__":
    game_menu()