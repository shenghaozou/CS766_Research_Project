func J = runDehazing(inputImage)
  I = inputImage;
  r = 10;
  beta = 1.0;
  % outputFolder = ['res/cross/' num2str(r) '_beta' num2str(beta)];
  outputFolder = ['res/' num2str(r) '_beta' num2str(beta)];
  mkdir(outputFolder);
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

  filename_depth = 'originalDepthMap.png';
  fullname_depth = fullfile(outputFolder, filename_depth);
  imwrite(dR, fullname_depth);
  % imwrite(dR, 'res/originalDepthMap.png');
  filename_refineD = 'refineDepthMap.png';
  fullname_refineD = fullfile(outputFolder, filename_refineD);
  imwrite(refineDR, fullname_refineD);
  % imwrite(refineDR, 'res/refineDepthMap.png');

  figure;
  imshow([dP dR refineDR]);
  title('depth maps');

  figure;
  imshow([tP tR]);
  title('transmission maps');

  filename_transmission = 'transmission.png';
  fullname_transmission = fullfile(outputFolder, filename_transmission);
  imwrite(tR, fullname_transmission);
  % imwrite(tR, 'res/refined_transmission.png');
  % add by Lin
  filename_rawTransmission = 'raw_transmission.png';
  fullname_rawTransmission = fullfile(outputFolder, filename_rawTransmission);
  imwrite(tP, fullname_rawTransmission);
  % imwrite(tP, 'res/raw_transmission.png');

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
end
