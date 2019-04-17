function br = BrightnessDetection(input_img)
    br = mean(sum(input_img, 3) / 3 / 255, 'all');
end
