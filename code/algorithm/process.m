function out_img = process(file_name)
    img = imread(file_name);
    img = AdvancedConstract(img);
    br = BrightnessDetection(img);
    if br < 0.8
        img = img + 255 * (0.8 - br);
    end
    out_img = img;
end