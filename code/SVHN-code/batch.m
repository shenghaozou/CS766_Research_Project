function batch(n)
    for i = 1:n
        file_src = "data/test/" + i + ".png";
        img = process(file_src);
        imwrite(img, "data/generated/" + i + ".png");
    end

end
