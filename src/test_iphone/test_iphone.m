% 
% %recherche du fichier
% %Le nom de repertoire a7d3ff69cc0ed6652bb2df789492ac86950c03eb est à
% %changer en fonction de votre iphone (pour cela, il suffit de reperer le
% %repoertoire dans l'explorateur windows et le remplacer dans la ligne du
% %dessous
% 
% cd C:\Users\Choc\AppData\Roaming\Apple' Computer'\MobileSync\Backup\a7d3ff69cc0ed6652bb2df789492ac86950c03eb
% 
% fprintf('Soyez patient, je recherche le bon fichier...\n');
% [status,result] =dos('findstr /M CellLocation *.*');
% %remove last space
% file=result(1:end-1);
% fprintf('OK, je l ai choppé, je le rapatrie donc...\n');
% copyfile(file,'C:\Users\Choc\Documents\MATLAB\code\test_iphone\map.sql');
% cd C:\Users\Choc\Documents\MATLAB\code\test_iphone;

%Recuperation de la base de donnée
mksqlite('open', 'map.sql');
result = mksqlite('select * from CellLocation');
mksqlite('close');
 
for indice=1:length(result)
    lat=result(indice).Latitude;
    long=result(indice).Longitude;
    G(indice,:)=[lat;long];
end
classe=kmeans(G,5);
%creation du fichier KML
for num_classe=1:5
     style=sprintf('style%d',num_classe);
    link=sprintf('http://maps.google.com/mapfiles/kml/paddle/%d_maps.png',num_classe);
    fid=fopen(sprintf('fichier%d.kml',num_classe), 'w');
    fprintf(fid,'<?xml version="1.0" encoding="UTF-8"?>\n');
    fprintf(fid,'<kml xmlns="http://www.opengis.net/kml/2.2"><Folder>\n');

    for indice=1:length(result)
        if (classe(indice)==num_classe)
        
            fprintf(fid,'<Placemark>\n');
            %fprintf(fid,'<name>Iphone Tracker</name>\n');
            lat=result(indice).Latitude;
            long=result(indice).Longitude;
            fprintf(fid,'<Style id="%s">\n',style);
            fprintf(fid,'<Icon>\n');
            fprintf(fid,'    <href>%s</href>\n',link);
            fprintf(fid,' </Icon>\n');
            fprintf(fid,'</Style>\n');
            fprintf(fid,'<Point>\n');
            fprintf(fid,'<coordinates>%f,%f,0</coordinates>\n',long,lat);
            fprintf(fid,'</Point>\n');
            fprintf(fid,'</Placemark>\n');
        end
    
    end
    fprintf(fid,'</Folder>\n');
    fprintf(fid,'</kml>\n');
    fclose(fid);
    clear fid
    winopen(sprintf('fichier%d.kml',num_classe));
end

