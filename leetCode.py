#\usr\bin\Python
# leetcode Hamming Distance problem
#https://leetcode.com/problems/hamming-distance/#/description

#using string manipulation
class Solution_string(object):
    def hammingDistance(self, x, y):
        """
        :type x: int
        :type y: int
        :rtype: int
        """
      
        #binary representation of each integer 
        bin_x = "{0:b}".format(x)
        bin_y = "{0:b}".format(y)
        
        #just to keep track of the differences
        count = 0
        
        # determine the max length and then place both strings in an equal length array
        maxlen = len(max(bin_x,bin_y))
		
        #pad out the strings to the longest length with letter x as a filler
        bin_x = '{s:{c}<{n}}'.format(s=bin_x,n=maxlen,c='x')
    	bin_y = '{s:{c}<{n}}'.format(s=bin_y,n=maxlen,c='x')

        #count the differences between the two variables
        for i in range(maxlen):
        	if bin_x[i] != bin_y[i]:
        		count += 1
        		        
        return count 
        
#using bitwise operators
class Solution(object):
	def hammingDistance(self,x,y):
		count = 0

		#do a bitwise OR, if there are any ones, those are the non-matching values
		xor = bin(int(x) ^ int(y))[2:]			
				
		#iterate each bit after AND
		for i in range(len(xor)):
			if (int(xor[i]) == 1): 
				count += 1
		
		return count
  
#test
sol = Solution()

x = 100
y = 40

print sol.hammingDistance(x,y)        