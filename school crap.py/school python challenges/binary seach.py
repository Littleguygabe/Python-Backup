nums = []

while True:
    num = input('___')
    if num == 'done':
        break

    else:
        nums.append(int(num))

unsorted = True

while unsorted:
    count = 0
    for i in range(0,len(nums)-1):
        if nums[i]>nums[i+1]:
            temp1 = nums[i]
            temp2 = nums[i+1]
            nums[i] = temp2
            nums[i+1] = temp1

            count+=1

        if count==0:
            unsorted = False
            break

        print(nums)

def binarySearch(nums):
    finding = int(input('search for:_ '))
    temppos = round(len(nums)/2)

    if finding>nums[temppos]:
        print(nums[temppos])
        del nums[0:temppos+1]
        print(nums)

    elif finding<nums[temppos]:
        print(nums[temppos])
        del nums[temppos:-1]
        print(nums)

    if finding==nums[temppos-1]:
        print(nums)
        print('found')
    
binarySearch(nums)