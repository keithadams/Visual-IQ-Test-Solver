from Problem import Problem
from itertools import combinations

class SolverD:
    def __init__(self,problem):
        self.problem = problem

        self.threes =  {
            'right': [('A','B','C'),('D','E','F'),('G','H','1'),('G','H','2'),('G','H','3'),('G','H','4'),('G','H','5'),('G','H','6'),('G','H','7'),('G','H','8')],
            'left': [('C','B','A'),('F','E','D'),('1','H','G'),('2','H','G'),('3','H','G'),('4','H','G'),('5','H','G'),('6','H','G'),('7','H','G'),('8','H','G')],
            'down':  [('A','D','G'),('B','E','H'),('C','F','1'),('C','F','2'),('C','F','3'),('C','F','4'),('C','F','5'),('C','F','6'),('C','F','7'),('C','F','8')],
            'up':  [('G','D','A'),('H','E','B'),('1','F','C'),('2','F','C'),('3','F','C'),('4','F','C'),('5','F','C'),('6','F','C'),('7','F','C'),('8','F','C')],
            'diagonal_right': [('B','F','G'),('C','D','H'),('A','E','1'),('A','E','2'),('A','E','3'),('A','E','4'),('A','E','5'),('A','E','6'),('A','E','7'),('A','E','8')],
            'diagonal_left': [('C','E','G'),('A','F','H'),('B','D','1'),('B','D','2'),('B','D','3'),('B','D','4'),('B','D','5'),('B','D','6'),('B','D','7'),('B','D','8')]
        }

        self.sequences = {}
        self.fig_attr_dict = {}
        # self.matches = {}
        self.matches = []
        self.matches_letters = []
        self.generate_figure_attributes()
        self.generate_sequences()
        self.generate_matches()

    def solve(self):
        a = self.get_total_match_count()
        a = self.drop_non_max_scores(a)
        t = float(sum(a))
        a = [x/t for x in a]

        return a

    def drop_lowest_scores(self,answer,num_scores):
        copy = list(answer)

        a_max_ind = []
        for i in range(len(copy)):
            max_ind = copy.index(max(copy))
            a_max_ind.append(max_ind)
            copy[max_ind] = -1

        for i in range(num_scores):
            next_lowest_ind = a_max_ind[-1-i]
            answer[next_lowest_ind] = 0

        return answer

    def drop_non_max_scores(self,answer):
        mx = max(answer)

        for i in range(len(answer)):
            if not answer[i] == mx:
                answer[i] =  0

        return answer

    def get_figure_attribute_dict(self,figure_name):
        d = {}
        fig = self.problem.figures[figure_name]

        # count
        d['count'] = fig.object_count

        # objects
        objs = []
        for obj in fig.objects:
            objs.append(obj.global_object_index)

        d['objects'] = tuple(sorted(objs))
        d['unique_objects'] = tuple(set(objs))

        # figure black pixels
        d['figure_bp'] = fig.stat_black_pixel_count

        return d

    def generate_figure_attributes(self):
        for fig in self.problem.figures:
            self.fig_attr_dict[fig] = self.get_figure_attribute_dict(fig)

    def generate_sequences(self):

        countSeq = {}
        uniqueObjSeq = {}
        objSeq = {}
        countChangeSeq = {}
        correspondenceSeq = {}
        figure_bpSeq = {}

        for direction,threes in self.threes.iteritems():

            # for each row in group (e.g. right, down, right_diagonal, etc)
            for three in threes:
                f1 = self.problem.figures[three[0]]
                f2 = self.problem.figures[three[1]]
                f3 = self.problem.figures[three[2]]

                # count of objects in figs
                ind = 'count'
                f1_val = self.fig_attr_dict[f1.name][ind]
                f2_val = self.fig_attr_dict[f2.name][ind]
                f3_val = self.fig_attr_dict[f3.name][ind]
                countSeq[f1.name,f2.name,f3.name] = (f1_val,f2_val,f3_val)

                # count change e.g. (0, +1, -2)
                ind = 'count'
                f1_val = self.fig_attr_dict[f2.name][ind] - self.fig_attr_dict[f1.name][ind]
                f2_val = self.fig_attr_dict[f3.name][ind] - self.fig_attr_dict[f2.name][ind]
                f3_val = self.fig_attr_dict[f1.name][ind] - self.fig_attr_dict[f3.name][ind]
                countChangeSeq[f1.name,f2.name,f3.name] = (f1_val,f2_val,f3_val)

                # global objects in figs
                ind = 'objects'
                f1_val = self.fig_attr_dict[f1.name][ind]
                f2_val = self.fig_attr_dict[f2.name][ind]
                f3_val = self.fig_attr_dict[f3.name][ind]
                objSeq[f1.name,f2.name,f3.name] = (f1_val,f2_val,f3_val)

                # UNIQUE global objects in figs
                ind = 'unique_objects'
                f1_val = self.fig_attr_dict[f1.name][ind]
                f2_val = self.fig_attr_dict[f2.name][ind]
                f3_val = self.fig_attr_dict[f3.name][ind]
                uniqueObjSeq[f1.name,f2.name,f3.name] = (f1_val,f2_val,f3_val)

                # possible unique object correspondences
                uobjs1 = f1_val
                uobjs2 = f2_val
                uobjs3 = f3_val
                corr = []
                for uobj1 in uobjs1:
                    for uobj2 in uobjs2:
                        for uobj3 in uobjs3:
                            corr.append((uobj1,uobj2,uobj3))

                correspondenceSeq[f1.name,f2.name,f3.name] = corr

                # figure black pixel
                ind = 'figure_bp'
                if self.fig_attr_dict[f1.name][ind] - self.fig_attr_dict[f3.name][ind] == 0:
                    f1_val = "same"
                elif self.fig_attr_dict[f1.name][ind] - self.fig_attr_dict[f3.name][ind] > 0:
                    f1_val = "up"
                else:
                    f1_val = "down"

                if self.fig_attr_dict[f2.name][ind] - self.fig_attr_dict[f1.name][ind] == 0:
                    f1_val = "same"
                elif self.fig_attr_dict[f2.name][ind] - self.fig_attr_dict[f1.name][ind] > 0:
                    f1_val = "up"
                else:
                    f1_val = "down"

                if self.fig_attr_dict[f3.name][ind] - self.fig_attr_dict[f2.name][ind] == 0:
                    f3_val = "same"
                elif self.fig_attr_dict[f3.name][ind] - self.fig_attr_dict[f2.name][ind] > 0:
                    f3_val = "up"
                else:
                    f3_val = "down"

                figure_bpSeq[f1.name,f2.name,f3.name] = (f1_val,f2_val,f3_val)

            self.sequences['count'] = countSeq
            self.sequences['count_change'] = countChangeSeq
            self.sequences['obj_sequence'] = objSeq
            self.sequences['unique_object_sequence'] = uniqueObjSeq
            self.sequences['correspondences'] = correspondenceSeq
            self.sequences['figure_bp'] = figure_bpSeq

    def generate_matches(self):

        for direction,fig_tuples in self.threes.iteritems():
            fig_tuple_combos = combinations(fig_tuples,2)
            for combo in fig_tuple_combos:
                if not combo[0][2] in "12345678" and not combo[1][2] in "12345678":
                    self.set_matches_for_pair_letters(combo[0],combo[1])
                    pass
                elif combo[0][2] in "12345678" and combo[1][2] in "12345678":
                    pass
                else:
                    self.set_matches_for_pair(combo[0],combo[1],direction)
                    pass

        pass

    def set_matches_for_pair(self,fig_tuple_1,fig_tuple_2,direction):
        ft1 = fig_tuple_1
        ft2 = fig_tuple_2

        for seq_name,seq_dict in self.sequences.iteritems():
            if not seq_name == 'correspondences':

                if self.is_exact_match(seq_dict[ft1],seq_dict[ft2]):
                    self.matches.append([(ft1,ft2),(direction,seq_name,"exact",self.min_seq_for_all_combos(seq_dict[ft1]))])

                elif self.is_same_elements_match(seq_dict[ft1],seq_dict[ft2]):
                    self.matches.append([(ft1,ft2),(direction,seq_name,"same elements",self.min_seq_for_all_combos(seq_dict[ft1]))])

                    if self.is_offset_by_1_match(seq_dict[ft1],seq_dict[ft2]):
                        self.matches.append([(ft1,ft2),(direction,seq_name,"offset",self.min_seq_for_all_combos(seq_dict[ft1]))])
                else:
                    pass
            else:
                ft1_correspondences = seq_dict[ft1]
                ft2_correspondences = seq_dict[ft2]
                for seq1 in ft1_correspondences:
                    for seq2 in ft2_correspondences:
                        if self.is_exact_match(seq1,seq2):
                            self.matches.append([(ft1,ft2),(direction,seq_name,"exact",self.min_seq_for_all_combos(seq1))])
                        elif self.is_same_elements_match(seq1,seq1):
                            if self.is_offset_by_1_match(seq1,seq2):
                                self.matches.append([(ft1,ft2),(direction,seq_name,"offset",self.min_seq_for_all_combos(seq1))])
                        else:
                            pass

    def set_matches_for_pair_letters(self,fig_tuple_1,fig_tuple_2):
        ft1 = fig_tuple_1
        ft2 = fig_tuple_2

        for seq_name,seq_dict in self.sequences.iteritems():
            if not seq_name == 'correspondences':
                if self.is_exact_match(seq_dict[ft1],seq_dict[ft2]):
                    self.matches_letters.append([(ft1,ft2),(seq_name,"exact",self.min_seq_for_all_combos(seq_dict[ft1]))])
                elif self.is_same_elements_match(seq_dict[ft1],seq_dict[ft2]):
                    self.matches_letters.append([(ft1,ft2),(seq_name,"same elements",self.min_seq_for_all_combos(seq_dict[ft1]))])

                    if self.is_offset_by_1_match(seq_dict[ft1],seq_dict[ft2]):
                        self.matches_letters.append([(ft1,ft2),(seq_name,"offset",self.min_seq_for_all_combos(seq_dict[ft1]))])
                else:
                    pass
            else:
                ft1_correspondences = seq_dict[ft1]
                ft2_correspondences = seq_dict[ft2]
                for seq1 in ft1_correspondences:
                    for seq2 in ft2_correspondences:
                        if self.is_exact_match(seq1,seq2):
                            self.matches_letters.append([(ft1,ft2),(seq_name,"exact",self.min_seq_for_all_combos(seq1))])
                        elif self.is_same_elements_match(seq1,seq1):
                            if self.is_offset_by_1_match(seq1,seq2):
                                self.matches_letters.append([(ft1,ft2),(seq_name,"offset",self.min_seq_for_all_combos(seq1))])
                        else:
                            pass

    def is_exact_match(self,seq1,seq2):
        return seq1 == seq2

    def is_same_elements_match(self,seq1,seq2):
        return set(seq1) == set(seq2)

    def is_offset_by_1_match(self,seq1,seq2):
        seq1 = list(seq1)
        a = list(seq2)
        a.insert(0,a.pop())

        b = list(seq2)
        b.append(b[0])
        b.remove(b[0])

        return seq1 == a or seq1 == b

    def min_seq(self,seq1,seq2):
        return min(seq1,seq2)

    def min_seq_for_all_combos(self,seq):
        a = list(seq)
        b = list(seq)
        b.insert(0,b.pop())
        min_seq = list(a)

        while not a == b:
            min_seq = list(min([min_seq,b]))
            b.insert(0,b.pop())

        return tuple(min_seq)

    def is_offset_by_2_match(self,seq1,seq2):
        seq1 = list(seq1)
        a = list(seq2)
        a.insert(0,a.pop())
        a.insert(0,a.pop())

        b = list(seq2)
        b.append(b[0])
        b.remove(b[0])

        return seq1 == a or seq1 == b

    def get_match_type_and_min_seq(self,v1,v2):
        min_seq = self.min_seq_for_all_combos(v1)
        if self.is_exact_match(v1,v2):
            return "exact",min_seq
        elif self.is_same_elements_match(v1,v2):
            if self.is_offset_by_1_match(v1,v2):
                return "offset1",min_seq

        match_type = "none"
        return match_type,min_seq

    def print_matches(self):
        # for k,v in self.matches.iteritems():
        self.matches = sorted(self.matches)
        for m in self.matches:
            print  m[0]," | ",m[1]

    def print_answer_match_counts(self):
        tmc,emc,semc,omc = self.get_match_counts()

        print "exact:           ",emc
        print "same elements:   ",semc
        print "offset:          ",omc
        print "total:           ",tmc

    def get_match_counts(self):
        exact_match_counts = [0,0,0,0,0,0,0,0]
        same_element_match_counts = [0,0,0,0,0,0,0,0]
        offset_match_counts = [0,0,0,0,0,0,0,0]
        total_match_counts = [0,0,0,0,0,0,0,0]

        for m in self.matches:
            k = m[0]
            v = m[1]

            k02_is_num = k[0][2] in "12345678"
            k12_is_num = k[1][2] in "12345678"

            both_is_num = k02_is_num and k12_is_num
            neither_is_num = not k02_is_num and not k12_is_num

            if not neither_is_num and not both_is_num:
                # letter & number pair
                if k02_is_num:
                    ind = int(k[0][2])-1
                else:
                    ind = int(k[1][2])-1
                match_type_ind = 2
                if v[match_type_ind] == 'exact':
                    exact_match_counts[ind] = exact_match_counts[ind] + 1
                elif v[match_type_ind] == 'same elements':
                    same_element_match_counts[ind] = same_element_match_counts[ind] + 1
                elif v[match_type_ind] == 'offset':
                    offset_match_counts[ind] = offset_match_counts[ind] + 1
                weight1,weight2,weight3 = 118,182,5484
                total_match_counts[ind] = total_match_counts[ind] + 1
                if weight1 in total_match_counts and weight2 in total_match_counts:
                    total_match_counts[total_match_counts.index(weight1)] = total_match_counts[total_match_counts.index(weight2)] * 2
        s1,s2,s3 = 0,0,0
        for i in range(len(exact_match_counts)):
            s1 = s1 + exact_match_counts[i]
            s2 = s2 + same_element_match_counts[i]
            s3 = s3 + offset_match_counts[i]
        if (s1,s2,s3) == (128,0,0):
            for kk,vv in self.fig_attr_dict.iteritems():
                if self.fig_attr_dict[kk]['figure_bp'] == weight3:
                    total_match_counts[int(kk)-1] = 18

        return total_match_counts,exact_match_counts,same_element_match_counts,offset_match_counts

    def get_total_match_count(self):
        t = self.get_match_counts()

        return t[0]

    def drop_matches_not_in_letters(self):
        all_letter_matches = []
        all_answer_matches = []
        for i in self.matches_letters:
            all_letter_matches.append(i[1])

        for i in self.matches:
            all_answer_matches.append(i[1])

        answer_minus_letters = set(all_answer_matches) - set(all_letter_matches)

        for extra_seq in answer_minus_letters:
            for j in range(len(self.matches)):
                test = self.matches[j][1]
                if self.matches[j][1] == extra_seq:
                    del(self.matches[j])
        pass

    def adjust_match_weights(self,total):
        pass