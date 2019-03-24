a = imread('84.png');

b = imsharpen(a, 'Radius',3,'Amount',3);

[m, n, channel] = size(a);
c = zeros(m, n, channel, 'uint8');

gray_img = rgb2gray(a);
thresh = 0.02;
edge_img = edge(gray_img, 'sobel', thresh);

edge_img_2 = false(size(edge_img));

for i = 1:m
    for j = 1:n
        if edge_img(i,j)
            for ki = -2:2
                for kj = -2:2
                    newi = i + ki;
                    newj = j + kj;
                    if newi >= 1 && newi <= m && newj >=1 && newj <= n
                        edge_img_2(newi, newj) = 1;
                    end
                end
            end
        end
    end
end

for i = 1:m
    for j = 1:n
        if edge_img_2(i,j) == 0
            c(i,j,:) = a(i,j,:);
        else
            c(i,j,:) = b(i,j,:);
        end
    end
end


figure;
subplot(1,4,1);
imshow(a), title('Original Image');
subplot(1,4,2);
imshow(b), title('Sharpened Image');
subplot(1,4,3); 
imshow(c), title('Improved');
subplot(1,4,4); 
imshow(edge_img_2); title('Sobel Edge Detection');