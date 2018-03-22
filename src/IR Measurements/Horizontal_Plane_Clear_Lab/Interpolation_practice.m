% example of interpolation using the Spherical Harmonic (SH) domain using
% impulse responses for microphones mounted on the surface of an ideal
% sphere

addpath(genpath('Interpolation of Circular Data'));
load('ir_standardised.mat');
grid_readings = csvread('/home/bngzl/Documents/Final Year Project/final_year_project/src/audio/rvrb_sweep_clear_lab/azimuth_clear_lab.csv');

ir_measure = ir_standardised(:,:,1:2:end); 
ir_interp_gt = ir_standardised(:,:,2:2:end); 

measure_grid_az_deg = grid_readings(1:2:end-1,1);  % Measured Grid

%measure_grid_az_deg = (0:10:350).'; % Spacing between each measurement 
interp_grid_az_deg = (5:10:355).';% Spacing between interpolated result 

fs = 48000;

% dimension of SH representation
maxShOrd = 18;
nSh = (maxShOrd+1)^2;
nShCirc = 2*maxShOrd + 1;

idc_circ = zeros(nShCirc,1);
idc_circ(1) = 1; %ord 0 component
for ord=1:maxShOrd % This is to select the SHs which are only affected by azimuth (outer few in the pyramid)
    idc_circ(1+(ord-1)*2 + [1 2]) =  1+ord^2 + ord + ord*[-1 1];
end

nAzMeasure = length(measure_grid_az_deg);
nAzInterp = length(interp_grid_az_deg);

% Inclination of Measurements: 
measure_grid_inc_deg = 90*ones(size(measure_grid_az_deg));
interp_grid_inc_deg = 90*ones(size(interp_grid_az_deg));

Ymeasure = sphBasis(deg2rad(measure_grid_az_deg),...
                    deg2rad(measure_grid_inc_deg),...
                    maxShOrd); %[nAzMeasure nSH]
                
Ymeasure = Ymeasure(:,idc_circ);%[nAzMeasure nShCirc] 

Yinterp = sphBasis(deg2rad(interp_grid_az_deg),...
                    deg2rad(interp_grid_inc_deg),...
                    maxShOrd); %[nAzInterp nSH]
                
Yinterp = Yinterp(:,idc_circ);%[nAzInterp nShCirc]
                                 
nSamples = size(ir_measure,1);
nFFT = nSamples;
tf_measure = rfft(ir_measure,nFFT,1); %[nFreq nSensors, nAzMeasure]
nFreq = size(tf_measure,1);
fscale = (0:nFreq-1).' * (fs/nFFT);

%% quick plot of data to check it makes sense
% irefchan refers to the channel used, in this case it is channel 2 that is
% plotted 
irefchan = 2; %with rotation applied, this sensor is aligned with x axis
figure;plot(squeeze(ir_measure(:,irefchan,:)))
legend(num2str(measure_grid_az_deg))
title('Quick Plot') 
%first arrival should be from 0 degrees

% the inverse matrix maps from observed values to SH coefficients
% Ymeasure is the SH basis vectors - basically the SH coefficients 
Yinv = pinv(Ymeasure);

%% do the transformation to SH domain
% Concentrate on just one microphone signal
% Rearranging data to plot azimuth against frequency
measuredData = permute(tf_measure(:,irefchan,:),[3 1 2]); %[nAzMeasure nFreq] 

% get the estimated SH cofficients
% SH Coefficients 
est_fnm = Yinv * measuredData;

% reconstruct
reconstructedData = Ymeasure * est_fnm;
ir_reconstructed = irfft(permute(reconstructedData,[2 3 1]),nFFT,1); %[nSamples,1,nAzMeasure]

% interpolate
interpolatedData = Yinterp * est_fnm;
ir_interpolated = irfft(permute(interpolatedData,[2 3 1]),nFFT,1); %[nSamples,1,nAzInterp]


%% plot the measured impulse responses and the reconstructed versions
figure;
plot(squeeze(ir_measure(:,irefchan,:)))
hold all;
plot(squeeze(ir_reconstructed(:,1,:)),':')
legend(num2str([measure_grid_az_deg;measure_grid_az_deg]))
title('Measured Impulse Responses and Reconstructed Versions') 
% hide all lines so that pairs can be turned on for comparison in plot browser window
lh = get(gca,'children');
set(lh,'visible','off')
set(gcf,'windowstyle','docked')

%% Comparing Interpolated with Measured Results at Interpolated Positions 

% based on the measured impulse responses
figure;
plot(squeeze(ir_interp_gt(:,irefchan,:)))
hold all;
plot(squeeze(ir_interpolated(:,1,:)),'--')
legend(num2str([interp_grid_az_deg;interp_grid_az_deg]))
title('Ground Truth Impulse Responses and Interpolated Versions') 
% hide all lines so that pairs can be turned on for comparison in plot browser window
lh = get(gca,'children');
set(lh,'visible','off')
set(gcf,'windowstyle','docked')
% Dotted lines are the interpolated versions
