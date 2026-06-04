n_iters = 50;
r = 0.1;
x = linspace(0, 1, 500);
yline = x;

f = @(x) r .* x .* (1 - x);   
y = f(x);

figure
while r<4
    clf                             
    plot(x, y, 'black', 'LineWidth', 1.5)
    hold on
    plot(x, yline, 'black', 'LineWidth', 1.5)
    xlabel('x')
    ylabel('y')
    title(sprintf('r = %.2f', r))   
    grid on
    axis square
    xlim([0 1]); ylim([0 1])        

    x0 = 0.1;                       
    y0 = 0;

    for index = 1:n_iters
        plot([x0 x0], [y0 f(x0)], 'r-')
        y0 = f(x0);
        plot([x0 y0], [y0 y0], 'r-')
        x0 = y0;
    end

    r = r + 0.01;
    pause(0.00001)
end