V <- matrix(c(0.008,-0.002,0.004,  -0.002,0.002,-0.002,  0.004,-0.002,0.008),nrow=3,ncol=3)
rf <- 0.01
u <- matrix(c(0.06,0.02,0.04),nrow=1,ncol=3)
mu.vec <- c(0.06,0.02,0.04)
x <- matrix(c(1/3,1/3,1/3),nrow=3,ncol=1)
p_u <- u%*%x
p_V <- sqrt(t(x)%*%V%*%x)
sigma.mat <- V

top.mat= cbind(2*sigma.mat, rep(1,3))
bot.vec = c(rep(1,3), 0)
Am.mat = rbind(top.mat,bot.vec)
b.vec = c(rep(0,3),1)
z.m.mat = solve(Am.mat)%*%b.vec
m.vec = z.m.mat[1:3,1]

sigma.inv.mat = solve(sigma.mat)
one.vec = rep(1,3)
mu.minus.rf <- mu.vec-rf*one.vec
top.mat = sigma.inv.mat%*%mu.minus.rf
bot.val = as.numeric(t(one.vec)%*%top.mat)
t.vec <- top.mat[,1]/bot.val
t_u < mu.vec%*%t.vec
t_V <- sqrt(t(t.vec)%*%V%*%t.vec)