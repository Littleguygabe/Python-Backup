# Definition for singly-linked list.
class ListNode(object):
     def __init__(self, val=0, next=None):
         self.val = val
         self.next = next


class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: Optional[ListNode]
        :type l2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        num1 = ''
        num2 = ''
        while l1:
            num1+=str(l1.val)
            l1 = l1.next

        while l2:
            num2+=str(l2.val)
            l2 = l2.next

        num1 = num1[::-1]
        num2 = num2[::-1]
        sumStr = str(int(num1)+int(num2))[::-1]
        sumLL = []
        for i in range(len(sumStr)):
            if i == 0:
                sumLL.append(ListNode(int(sumStr[i])))

            else:
                sumLL.append(ListNode(int(sumStr[i])))
                sumLL[i-1].next = sumLL[i]

        return sumLL[0]

