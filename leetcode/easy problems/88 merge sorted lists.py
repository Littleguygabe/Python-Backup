def merge(nums1,nums2,n,m):
    for i in range(n):
        nums1[m+i] = nums2[i]
    nums1.sort()

    return nums1
nums1 = [1,2,3,0,0,0]
m = 3
nums2 = [2,5,6]
n = 3

merge(nums1,nums2,n,m)