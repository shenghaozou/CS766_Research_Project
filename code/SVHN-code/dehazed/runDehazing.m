function J = runDehazing(inputImage)
  I = inputImage;
  r = 10;
  beta = 1.0;
  % outputFolder = ['res/cross/' num2str(r) '_beta' num2str(beta)];
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
