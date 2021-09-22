# print(sum(map(lambda x:x if 0 in[x%3,x%5] else 0, list(range(1000)))))

asum=lambda n:n*(n+1)//2
gsum=lambda l:lambda x:x*asum((l-1)//x)
psum=gsum(10**100000)
print(psum(3)+psum(5)-psum(15))