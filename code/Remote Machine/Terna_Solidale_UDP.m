clc;
clear all;
disp("Attendo che la calibrazione dei sensori termini");
u = udp('192.168.1.107','LocalPort',28000,'Timeout',1000);
u.InputBufferSize = 1;
fopen(u);
aknowledge = fread(u,1);
disp("Calibrazione sensori terminata. Ora inizio a raccogliere i dati e plottarli.")
fclose(u);
u.Timeout = 10;
u.InputBufferSize = 12;
p = figure;
ax = axes('XLim',[-1.5 1.5],'YLim',[-1.5 1.5],'ZLim',[-1.5 1.5]);
view(3);
grid on;
hold on;
ButtonH=uicontrol('Parent',p,'Style','togglebutton','String','Termina Acquisizione','Units','normalized','Position',[0.0 0.0 0.2 0.2],'Visible','on');
hold on;

%INIZIALIZZO IL SISTEMA SOLIDALE CON QUELLO FISSO
%Versori sistema fisso
i = [1;0;0];
j = [0;1;0];
k = [0;0;1];
%Matrici utilizzate per plottare gli assi
Mx = [0 i(1);
      0 i(2);
      0 i(3)];
My = [0 j(1);
      0 j(2);
      0 j(3)];
Mz = [0 k(1); 0 k(2);0 k(3)];
%asse x 
x = plot3(Mx(1,:),Mx(2,:),Mx(3,:),'k');
hold on;
%asse y
y = plot3(My(1,:),My(2,:),My(3,:),'k');
hold on;
%asse z
z = plot3(Mz(1,:),Mz(2,:),Mz(3,:),'k');
hold on;
h(1) = plot3(Mx(1,:),Mx(2,:),Mx(3,:),'b');
hold on;
%asse y
h(2) = plot3(My(1,:),My(2,:),My(3,:),'r');
hold on;
%asse z
h(3) = plot3(Mz(1,:),Mz(2,:),Mz(3,:),'m');
hold on;
%PLOTTO UN CUBO CHE SARA' ANCHE ESSO SOLIDALE AL CORPO RIGIDO
%Vertici del parallelepipedo
AS = [sqrt(2)/2;-sqrt(2)/2;-sqrt(2)/2]; 
BS = [sqrt(2)/2;sqrt(2)/2;-sqrt(2)/2];
CS = [sqrt(2)/2;sqrt(2)/2;sqrt(2)/2];
DS = [sqrt(2)/2;-sqrt(2)/2;sqrt(2)/2];
ES = [-sqrt(2)/2;-sqrt(2)/2;-sqrt(2)/2]; 
FS = [-sqrt(2)/2;sqrt(2)/2;-sqrt(2)/2];
GS = [-sqrt(2)/2;sqrt(2)/2;sqrt(2)/2];
HS = [-sqrt(2)/2;-sqrt(2)/2;sqrt(2)/2];
AD_1 = [DS CS BS AS DS HS ES AS];
AD_2 = [FS ES HS GS FS BS CS GS];
h(4) = plot3(AD_1(1,:),AD_1(2,:),AD_1(3,:),'k');
hold on;
h(5) = plot3(AD_2(1,:),AD_2(2,:),AD_2(3,:),'k');
hold on;
%RAGRUPPO TUTTO IN UN UNICO OGGETTO
t = hgtransform('Parent',ax);
set(h,'Parent',t)
pause(0.00001)
while ~get(ButtonH,'Value')
    %Prelevo pacchetto
    fopen(u);
    angles_packed = fread(u,12);
    fclose(u);   
    %Prelevo gli angoli
    roll_packed = angles_packed(1:4);
    pitch_packed = angles_packed(5:8);
    yaw_packed = angles_packed(9:12);
    %Decodifico i dati
    phi = typecast(uint8(roll_packed),'single');
    theta = typecast(uint8(pitch_packed),'single');
    psi = typecast(uint8(yaw_packed),'single');
    %Calcolo matrici di rotazione. Devono essere calcolate tenendo conto
    %che la matrice finale rappresenta una successione estrinseca, invece
    %quella che si e calcolata con l' IMU era di tipo intrinseco.
    Rz = makehgtform('zrotate',psi);
    Ry = makehgtform('yrotate',theta);
    Rx = makehgtform('xrotate',phi);
    %Assegno la matrice alla proprieta Matrix dell' oggetto associato alla
    %figura da ruotare
    set(t,'Matrix',Rz*Ry*Rx);
    %Disegno il nuovo sistema e parallelepipedo solidale
    drawnow
end
fclose(u);
