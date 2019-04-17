function batch(n, basedir)
    % basedir = "/Volumes/external/data/test";
    parfor i = 1:n
        file_src = fullfile(basedir, "test",  i + ".png");
        img = process(file_src);
        file_dst = fullfile(basedir, "generated",  i + ".png")
        imwrite(img, file_dst);
    end
end
