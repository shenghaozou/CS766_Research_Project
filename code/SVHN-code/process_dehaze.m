function out_img = process(file_name)
    img = imread(file_name);
    out_img = runDehazing(img);
end
