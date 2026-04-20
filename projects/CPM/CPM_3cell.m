function CPM_3cell
    %file name prefix
    name='figure';
    
    %initialise lattice parameters
    gridWidth=150;
    nCells=3;

    %initialise simulation parameters
    lambdaV=1;
    T=1;
    targetVolume=[0 2500 2500,2500];
    J = [ 0  1 10 10;
          1  0  1  5;
         10  1  0  1;
         10  5  1  0];

 
    %defines neighbour directions, the Moore 8-neighbourhood 
    NEIGHBORS=[
        -1 -1;
        -1  0;
        -1  1;
         0 -1;
         0  1;
         1 -1;
         1  0;
         1  1];

    volumes=[];
    palette=[];

    %sets random number seed for reproducibility
    rng(2);

    %prepares directory for saving frames
    if exist(name, 'dir')
        delete(fullfile(name, '*'));
    else
        mkdir(name);
    end

    %initialises the lattice
    create_palette();
    lattice=zeros(gridWidth, gridWidth);
    set_initial();

    %plots the lattice and save the first frame
    fig = figure;
    axL=axes(fig);
    hIm=imagesc(axL, lattice);
    axis(axL, 'image');
    set(axL, 'XTick', [], 'YTick', []);
    colormap(axL, palette);
    clim(axL, [0, nCells]);
    title(axL, {
    'Time = 0 MCS' ...
    ['$\lambda_V=$', num2str(lambdaV)] ...
    ['$T=$', num2str(T)]}, 'Interpreter', 'latex','FontSize', 20,'FontWeight', 'bold');
    exportgraphics(axL, fullfile(sprintf(name), sprintf('%s_0.png', name)));

    %begin the main update loop
    maxFrames=2500;
    for frame = 1:maxFrames
        %updates lattice with a sweep
        n_attempts=(gridWidth^2);
        for k=1:n_attempts
            updateCells();
        end
        
        %display the updated lattice
        set(hIm, 'CData', lattice);
         title(axL, {
            ['Time = ', num2str(frame), ' MCS'] ...
            ['$\lambda_V=$', num2str(lambdaV)] ...
            ['$T=$', num2str(T)]}, 'Interpreter', 'latex','FontSize', 20,'FontWeight', 'bold');
        drawnow;

        %saves every 10th frame
        if mod(frame, 10)==0
            exportgraphics(axL, fullfile(sprintf(name), sprintf('%s_%d.png', name, frame)));
        end
    end
    
    %dynamically creates a colour palette based on the number of cell types
    function create_palette()
        palette=zeros(nCells+1, 3);
        palette(1, :)=[1, 1, 1];
        if nCells==1
            palette(2, :) = [0 0 0];
        else
            for t=1:nCells
                h=(t-1)/max(1, (nCells-1))*(20/36);
                palette(t+1, :)=hsv2rgb([h, 1, 1]);
            end
        end
    end

    %creates a circular region of randomly distributed cell types
    function set_initial()
        cent=gridWidth/2;
        
        %checks if every lattice site falls within a circle at the center
        %of the lattice. If so assign it a random cell type
        for r=1:gridWidth
            for c=1:gridWidth
                dx=c-cent;
                dy=r-cent;
                dist=sqrt(dx^2+dy^2);

                radius=gridWidth*0.3;

                if dist<radius
                    t=randi([1, nCells]);
                    lattice(r, c)=t;
                end
            end
        end

        %calculates initial volumes of cell types
        edges=0:(nCells + 1);
        volumes=histcounts(lattice(:), edges);
    end

    %choses a random neighbor of the given lattice site (r,c)
    function nbr = getRandomNeighbor(r, c)
    i = randi(size(NEIGHBORS,1));

    new_r = mod(r + NEIGHBORS(i,1) - 1, gridWidth) + 1;
    new_c = mod(c + NEIGHBORS(i,2) - 1, gridWidth) + 1;

    nbr = [new_r, new_c];
end

    %find the change in energy from changing the cell type of (r,c) into
    %new_type
    function dH=deltaH(r, c, new_type)
        oldType=lattice(r, c);
        
        %no energy change if cell doesnt change
        if oldType==new_type
            dH=0;
            return;
        end

        %initialises the components of dH
        dH_adhesion=0;
        dH_volume=0;

        
        %finds the change in adhesion caused by changinf the cell type at
        % (r,c) from oldType to new_type by summing differences in contact 
        % energy with each neighbor
        for i=1:size(NEIGHBORS, 1)
            nr=NEIGHBORS(i, 1);
            nc=NEIGHBORS(i, 2);

            new_r = mod(r+nr-1,gridWidth)+1;
            new_c = mod(c+nc-1,gridWidth)+1;

            nType=lattice(new_r, new_c);

            delta_old=(oldType==nType);
            delta_new=(new_type==nType);

            contact_before=J(oldType+1, nType+1)*(1-delta_old);
            contact_after=J(new_type+1, nType+1)*(1-delta_new);

            dH_adhesion=dH_adhesion+(contact_after-contact_before);
        end

        
        % store current and new volumes by type
        vOld=volumes(oldType+1);
        vNew=volumes(new_type+1);
        % store current and new target volumes by type 
        VOld=targetVolume(oldType+1);
        VNew=targetVolume(new_type+1);

        %energy change from removing one cell from the old type
        if oldType~= 0
            beforeOld=vOld-VOld;
            afterOld=(vOld-1)-VOld;
            dH_volume=dH_volume+lambdaV*(afterOld^2-beforeOld^2);
        end
        % energy change from adding one cell to the new type
        if new_type~=0
            beforeNew=vNew-VNew;
            afterNew=(vNew+1)-VNew;
            dH_volume=dH_volume+lambdaV*(afterNew^2-beforeNew^2);
        end
        
        %finds total change in Hamiltonian  
        dH=dH_adhesion+dH_volume;
    end

    %main update logic
    function updateCells()
        %selects a random lattice site and selects a random neighbor 
        r=randi(gridWidth);
        c=randi(gridWidth);
        nbr=getRandomNeighbor(r, c);

        nr=nbr(1);
        nc=nbr(2);
        
        oldType=lattice(r, c);
        newType=lattice(nr, nc);

        if oldType==newType
            return;
        end
        
        %finds change in energy from proposed change
        dH=deltaH(r, c, newType);
        
        %Metropolis Hastings step
        if dH<=0 || rand<exp(-dH/T)
            lattice(r, c)=newType;
            volumes(oldType+1)=volumes(oldType+1)-1;
            volumes(newType+1)=volumes(newType+1)+1;
        end
    end
end