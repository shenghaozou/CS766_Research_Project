function batch(n)
    for i = 1:n
        file_src = "/Volumes/external/data/test/test/" + i + ".png";
        img = process(file_src);
        imwrite(img, "/Volumes/external/data/test/generated/" + i + ".png");
    end

end