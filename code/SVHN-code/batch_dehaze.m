function batch_dehaze(n, basedir)
    % basedir = "/Volumes/external/data/test";
    addpath('./dehazed')
    for i = 1:n
        file_src = fullfile(basedir, "test",  i + ".png");
        img = process_dehaze(file_src);
        file_dst = fullfile(basedir, "generated",  i + ".png")
        imwrite(img, file_dst);
    end
end
