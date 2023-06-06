clc
clear all



filename = input('Inserisci segnale non filtrato: ','s');
ID = fopen(filename,'r');
raw = fscanf(ID,'%f',[Inf]);
fclose(ID);

filename = input('Inserisci segnale filtrato: ','s');
ID = fopen(filename,'r');
filtered = fscanf(ID,'%f',[Inf]);
fclose(ID);


figure;

p1 = plot(raw,'b');
hold on;
p2 = plot(filtered,'r');
p2.Marker = '.';
p2.LineStyle = 'none';
grid on;
title('Segnale grezzo e filtrato');
xlabel('Numero campione segnale');
ylabel('Valore campione segnale');
set(gca,'Color','k')