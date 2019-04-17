function dehaze(I,outputDir, index)

% inputImagePath = 'inputImgs/cityscape_input.png';
% I = imread(inputImagePath);
% I = input;
% filename_depth = [sprintf('%03doriginalDepthMap',index) '.jpg'];
% fullname_depth = fullfile(outputDir,'images',filename_depth);
% filename_refineDepth = [sprintf('%03drefineDepthMap',index) '.jpg'];
% fullname_refineDepth = fullfile(outputDir,'images',filename_refineDepth);
% filename_transmission = [sprintf('%03dtransmission',index) '.jpg'];
% fullname_transmission = fullfile(outputDir,'images',filename_transmission);
% filename_rawTransmission = [sprintf('%03drawTransmission',index) '.jpg'];
% fullname_rawTransmission = fullfile(outputDir,'images',filename_rawTransmission);

filename = [sprintf('%03d',index) '.jpg'];
fullname = fullfile(outputDir,filename);

r = 20;
beta = 1.2;

%----- Parameters for Guided Image Filtering -----
gimfiltR = 60;
eps = 10^-3;
%-------------------------------------------------
tic;
[dR, dP] = calVSMap(I, r);
refineDR = fastguidedfilter_color(double(I)/255, dP, r, eps, r/4);
%refineDR = imguidedfilter(dR, double(I)/255, 'NeighborhoodSize', [gimfiltR, gimfiltR], 'DegreeOfSmoothing', eps);
tR = exp(-beta*refineDR);
tP = exp(-beta*dP);

% imwrite(dR, 'res/originalDepthMap.png');
% imwrite(refineDR, 'res/refineDepthMap.png');
% imwrite(dR, fullname_depth);
% imwrite(refineDR, fullname_refineDepth);


figure;
% imshow([dP dR refineDR]);
title('depth maps');

figure;
% imshow([tP tR]);
title('transmission maps');
% imwrite(tR, 'res/refined_transmission.png');
% imwrite(tR, fullname_transmission);
% add by Lin
% imwrite(tP, 'res/raw_transmission.png');
% imwrite(tP, fullname_rawTransmission);
a = estA(I, dR);
t0 = 0.05;
t1 = 1;
I = double(I)/255;
[h w c] = size(I);
J = zeros(h,w,c);
J(:,:,1) = I(:,:,1)-a(1);
J(:,:,2) = I(:,:,2)-a(2);
J(:,:,3) = I(:,:,3)-a(3);

t = tR;
[th tw] = size(t);
for y=1:th
    for x=1:tw
        if t(y,x)<t0
            t(y,x)=t0;
        end
    end
end

for y=1:th
    for x=1:tw
        if t(y,x)>t1
            t(y,x)=t1;
        end
    end
end

J(:,:,1) = J(:,:,1)./t;
J(:,:,2) = J(:,:,2)./t;
J(:,:,3) = J(:,:,3)./t;

J(:,:,1) = J(:,:,1)+a(1);
J(:,:,2) = J(:,:,2)+a(2);
J(:,:,3) = J(:,:,3)+a(3);

toc;
% figure;
% imshow([I J]);
% title('hazy image and dehazed image');

saveName = ['res/' num2str(r) '_beta' num2str(beta) '.png'];
% imwrite(J, saveName);
imwrite(J, fullname);
end