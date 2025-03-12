def lengthOfLongestSubstring(s):
    """
    :type s: str
    :rtype: int
    """
    l = len(s)


    longestSubString = ''
    for i in range(l):
        substring = ''
        if l-i<len(substring):
            return len(substring)            
        for j in range(i,l):
            if s[j] not in substring:
                substring+=s[j]
            else:
                if len(substring)>len(longestSubString):
                    longestSubString = substring
                    break

    if len(longestSubString) == 0:
        return 1
    
    return len(longestSubString)
                    

print(lengthOfLongestSubstring(' '))