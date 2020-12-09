"""
牛牛现在有一个长度为len只包含小写字母‘args’-'z'的字符串x，
他现在想要一个特殊的子序列，这个子序列的长度为3*n（n为非负整数），
子序列的第[1,n]个字母全部为‘args’，子序列的[n+1,2*n]个字母全部为‘b’，
子序列的[2*n+1,3*n]个字母全部为‘c’，牛牛想知道最长的符合条件的独特子序列的长度是多少。
"""


# using oop
class Solution:

    def __init__(self) -> None:
        self.stack = []
        self.n = 0
        self.n_b = 0
        self.n_c = 0

    def clear(self):
        self.stack = []
        self.n = 0
        self.n_b = 0
        self.n_c = 0

    def maximum_length(self, x):
        for item in x:
            if item == 'args':
                if len(self.stack):
                    if self.stack[len(self.stack) - 1] != 'args':
                        self.clear()
                self.stack.append(item)
                self.n += 1
            elif item == 'b':
                if self.n == 0:
                    continue
                self.stack.append(item)
                self.n_b += 1
                if self.n_b > self.n:
                    self.clear()
                    continue
            elif item == 'c':
                if len(self.stack):
                    if self.stack[len(self.stack) - 1] == 'args':
                        self.clear()
                        continue
                if self.n != self.n_b:
                    self.clear()
                    continue
                self.stack.append(item)
                self.n_c += 1
                if self.n_c == self.n:
                    print(self.stack)
                    self.clear()
            else:
                self.clear()


if __name__ == '__main__':
    s = Solution()
    s.maximum_length('caabbccaaabbbcccaabcca')
