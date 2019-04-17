function out_img = process(file_name)
    img = imread(file_name);
    img = AdvancedConstract(img);
    br = BrightnessDetection(img);
    img = img + 255 * (0.5 - br);
    out_img = img;
end
