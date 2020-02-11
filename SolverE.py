from ImageProcessing import *
from Object import Object


class SolverE:
    def __init__(self,problem):
        self.problem = problem
        self.transition_scores = {}

        self.threes_letters =  {
            'right': [('A','B','C'),('D','E','F')],
            # 'left': [('C','B','A'),('F','E','D')],
            # 'up':  [('G','D','A'),('H','E','B')],
            'down':  [('A','D','G'),('B','E','H')]
        }
        self.add_count = 0
        self.subtract_pixel_count = 0
        self.xor_count = 0
        self.comp_count = 0
        self.and_count = 0
        self.total_count = 0

    def solve(self):

        # print "============================"
        # print self.problem.name
        # print "============================"

        for direction in self.threes_letters.itervalues():
            for three_row in direction:
                f1 = self.problem.figures[three_row[0]]
                f2 = self.problem.figures[three_row[1]]
                f3 = self.problem.figures[three_row[2]]

                self.set_add_image_score(f1,f2,f3)
                self.set_xor_image_score(f1,f2,f3)
                self.set_subtract_pixel_score(f1,f2,f3)
                self.set_comp_score(f1,f2,f3)
                self.set_and_score(f1,f2,f3)

                self.total_count = self.add_count + self.subtract_pixel_count + self.xor_count + self.comp_count +self.and_count

                # self.transition_scores[three_row]

        # print "add", self.add_count
        # print "subtract_pixel_count:", self.subtract_pixel_count
        # print "self.xor_count:", self.xor_count
        # print "self.comp_count:", self.comp_count
        # print "self.and_count:", self.and_count
        answer = [0,0,0,0,0,0,0,0]

        if self.add_count > 0:
            best_add_answers = self.get_best_add_answers()
            for bai in best_add_answers:
                answer[bai[0]] = 1.0
            return answer
        elif self.and_count > 0:
            best_and_answers = self.get_best_and_answers()
            for bai in best_and_answers:
                answer[bai[0]] = 1.0
            return answer

        elif self.xor_count > 0 and self.xor_count >= self.subtract_pixel_count:
            best_xor_answers = self.get_best_xor_answers()
            for bai in best_xor_answers:
                answer[bai[0]] = 1.0
            return answer
        elif self.subtract_pixel_count > 0:
            best_subtract_pix_answers = self.get_best_subtract_pixel_answers()
            for bai in best_subtract_pix_answers:
                answer[bai[0]] = 1.0
            return answer
        elif self.comp_count > 0:
            best_comp_answers= self.get_best_comp_answers()
            for bai in best_comp_answers:
                answer[bai[0]] = 1.0
            return answer
        else:
            return [0.125,.125,.125,.125,.125,.125,.125,.125]

    def detect_add(self,fig1,fig2,fig3):
        img1 = fig1.img_uncropped
        img2 = fig2.img_uncropped
        img3 = fig3.img_uncropped

        added = add_images(img1,img2)

        isEqual = Object.is_equal_image_comparison(added,img3)
        rms = rmsdiff(added,img3)
        return isEqual,rms

    def detect_and(self,fig1,fig2,fig3):
        img1 = fig1.img_uncropped
        img2 = fig2.img_uncropped
        img3 = fig3.img_uncropped


        anded = and_images(img1,img2)


        # isEqual = Object.is_equal_image_comparison(anded,img3)
        rms = rmsdiff(anded,img3)
        if rms < 30:
            isEqual = True
        else:
            isEqual = False

        return isEqual,rms

    def detect_xor(self,fig1,fig2,fig3):
        img1 = fig1.img_uncropped
        img2 = fig2.img_uncropped
        img3 = fig3.img_uncropped

        xor = xor_images(img1,img2)

        isEqual = Object.is_equal_image_comparison(xor,img3)
        rms = rmsdiff(xor,img3)
        return isEqual,rms

    def detect_subtract_pixel(self,fig1,fig2,fig3):
        bp1 = fig1.stat_black_pixel_count
        bp2 = fig2.stat_black_pixel_count
        bp3 = fig3.stat_black_pixel_count

        subtracted_pix = bp1-bp2

        ratio = min(bp3,subtracted_pix)/max(bp3,subtracted_pix)

        if ratio > .95:
            isEqual = True
        else:
            isEqual = False

        return isEqual,ratio

    def detect_comp(self,fig1,fig2,fig3):
        img1 = fig1.img_uncropped
        img2 = fig2.img_uncropped
        img3 = fig3.img_uncropped

        comp = top1_bottom2_comp(img1,img2)

        isEqual = Object.is_equal_image_comparison(comp,img3)
        rms = rmsdiff(comp,img3)
        return isEqual,rms

    def set_add_image_score(self,fig1,fig2,fig3):
        isEqual,rms = self.detect_add(fig1,fig2,fig3)

        if isEqual:
            self.add_count = self.add_count + 1
            self.transition_scores[(fig1.name,fig2.name,fig3.name)] = ('add',0.0)
        elif rms < 10:
            self.add_count = self.add_count + 1
            self.transition_scores[(fig1.name,fig2.name,fig3.name)] = ('add',rms)

    def set_and_score(self,fig1,fig2,fig3):
        isEqual,rms = self.detect_and(fig1,fig2,fig3)

        if isEqual:
            self.and_count = self.and_count + 1
            self.transition_scores[(fig1.name,fig2.name,fig3.name)] = ('and',0.0)
        elif rms < 10:
            self.and_count = self.and_count + 1
            self.transition_scores[(fig1.name,fig2.name,fig3.name)] = ('and',rms)

    def set_comp_score(self,fig1,fig2,fig3):
        isEqual,rms = self.detect_comp(fig1,fig2,fig3)

        if isEqual:
            self.comp_count = self.comp_count + 1
            self.transition_scores[(fig1.name,fig2.name,fig3.name)] = ('comp',0.0)
        elif rms < 10:
            self.comp_count = self.comp_count + 1
            self.transition_scores[(fig1.name,fig2.name,fig3.name)] = ('comp',rms)

    def set_xor_image_score(self,fig1,fig2,fig3):
        isEqual,rms = self.detect_xor(fig1,fig2,fig3)

        if isEqual:
            self.xor_count = self.xor_count + 1
            self.transition_scores[(fig1.name,fig2.name,fig3.name)] = ('xor',0.0)
        elif rms < 40:
            self.xor_count = self.xor_count + 1
            self.transition_scores[(fig1.name,fig2.name,fig3.name)] = ('xor',rms)

    def set_subtract_pixel_score(self,fig1,fig2,fig3):
        isEqual,ratio = self.detect_subtract_pixel(fig1,fig2,fig3)

        if isEqual:
            self.subtract_pixel_count = self.subtract_pixel_count + 1
            self.transition_scores[(fig1.name,fig2.name,fig3.name)] = ('subtract_pixel',0.0)
        # elif rms < 10:
        #     self.add_count = self.add_count + 1
        #     self.transition_scores[(fig1.name,fig2.name,fig3.name)] = ('subtract_pixel',rms)

    def get_best_add_answers(self):
        candidates = []
        for c in "12345678":
            fig1 = self.problem.figures['G']
            fig2 = self.problem.figures['H']
            fig3 = self.problem.figures[c]

            isEqual,rms = self.detect_add(fig1,fig2,fig3)
            candidates.append((c,rms,isEqual))

            fig1 = self.problem.figures['C']
            fig2 = self.problem.figures['F']
            fig3 = self.problem.figures[c]

            isEqual,rms = self.detect_add(fig1,fig2,fig3)
            candidates.append((c,rms,isEqual))

        best_candidates,rms = self.get_best_candidates_as_indices(candidates)

        bc = []
        for l in best_candidates:
            bc.append((l,rms))
        return bc

    def get_best_and_answers(self):
        candidates = []
        for c in "12345678":
            fig1 = self.problem.figures['G']
            fig2 = self.problem.figures['H']
            fig3 = self.problem.figures[c]

            isEqual,rms = self.detect_and(fig1,fig2,fig3)
            candidates.append((c,rms,isEqual))

            fig1 = self.problem.figures['C']
            fig2 = self.problem.figures['F']
            fig3 = self.problem.figures[c]

            isEqual,rms = self.detect_and(fig1,fig2,fig3)
            candidates.append((c,rms,isEqual))

        best_candidates,rms = self.get_best_candidates_as_indices(candidates)

        bc = []
        for l in best_candidates:
            bc.append((l,rms))
        return bc

    def get_best_comp_answers(self):
        candidates = []
        for c in "12345678":
            fig1 = self.problem.figures['G']
            fig2 = self.problem.figures['H']
            fig3 = self.problem.figures[c]

            isEqual,rms = self.detect_comp(fig1,fig2,fig3)
            candidates.append((c,rms,isEqual))

            fig1 = self.problem.figures['C']
            fig2 = self.problem.figures['F']
            fig3 = self.problem.figures[c]

            isEqual,rms = self.detect_comp(fig1,fig2,fig3)
            candidates.append((c,rms,isEqual))

        best_candidates,rms = self.get_best_candidates_as_indices(candidates)

        bc = []
        for l in best_candidates:
            bc.append((l,rms))
        return bc

    def get_best_xor_answers(self):
        candidates = []
        for c in "12345678":
            fig1 = self.problem.figures['G']
            fig2 = self.problem.figures['H']
            fig3 = self.problem.figures[c]

            isEqual,rms = self.detect_xor(fig1,fig2,fig3)
            candidates.append((c,rms,isEqual))

            fig1 = self.problem.figures['C']
            fig2 = self.problem.figures['F']
            fig3 = self.problem.figures[c]

            isEqual,rms = self.detect_xor(fig1,fig2,fig3)
            candidates.append((c,rms,isEqual))

        best_candidates,rms = self.get_best_candidates_as_indices(candidates)

        bc = []
        for l in best_candidates:
            bc.append((l,rms))
        return bc

    def get_best_subtract_pixel_answers(self):
        candidates = []
        for c in "12345678":
            fig1 = self.problem.figures['G']
            fig2 = self.problem.figures['H']
            fig3 = self.problem.figures[c]

            isEqual,ratio = self.detect_subtract_pixel(fig1,fig2,fig3)
            candidates.append((c,1-ratio,isEqual))

            fig1 = self.problem.figures['C']
            fig2 = self.problem.figures['F']
            fig3 = self.problem.figures[c]

            isEqual,ratio = self.detect_subtract_pixel(fig1,fig2,fig3)
            candidates.append((c,1-ratio,isEqual))

        best_candidates,ratio = self.get_best_candidates_as_indices(candidates)

        bc = []
        for l in best_candidates:
            bc.append((l,ratio))
        return bc

    def get_best_candidates_as_indices(self,candidates):
        cand_rms = [0,0,0,0,0,0,0,0]
        for i in range(len(candidates)):
            c,rms,isEqual = candidates[i]
            ind = int(c)-1
            cand_rms[ind] = cand_rms[ind] + rms

        mn = min(cand_rms)
        index = []
        for i in range(len(cand_rms)):
            if cand_rms[i] == mn:
                index.append(i)

        return index,mn

    def get_seq_membership(self,fig1,fig2,fig3):
        if (fig1.name,fig2.name,fig3.name) in self.threes_letters['right']:
            return 'right'
        elif (fig1.name,fig2.name,fig3.name) in self.threes_letters['down']:
            return 'left'

