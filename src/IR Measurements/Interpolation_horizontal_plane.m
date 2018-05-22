% example of interpolation using the Spherical Harmonic (SH) domain using
% impulse responses for microphones mounted on the surface of an ideal
% sphere

clear all;

% Loading Data: 
addpath(genpath('Interpolation of Circular Data'));
load('ir_standardised_horizontal_plane_909b.mat'); % Obtained from IR_Standardisation.m

% Initialise recorded impulse response data from ir_standardised 
% Last column is the directions measured 
ir_measure = ir_standardised(:,:,1:2:end); % matrix with audio data from every 10 degrees starting from 0 to 350
                                           % nDirections: 36 
ir_interp_gt = ir_standardised(:,:,2:2:end); % matrix with audio data from every 10 degrees starting from 5 to 355
                                           % nDirections: 36

grid_readings = csvread('/home/bngzl/Documents/Final Year Project/final_year_project/src/Past Measurements/909b Horizontal Plane 1/Audio/rvrb_sweep_909b/azimuth_909b.csv');

% Ideal Grid: 
%measure_grid_az_deg = (0:10:350).'; % Ideal Grid
measure_grid_az_deg = grid_readings(1:2:end-1,1); % Measured Grid

%interp_grid_az_deg = (5:10:355).';% Spacing between interpolated result 
interp_grid_az_deg = grid_readings(2:2:end,1); % Interpolated Grid so can compare with actual measurements better

fs = 48000;

% dimension of SH representation
maxShOrd = 18; % Maximum Spherical Harmonic Order 
nSh = (maxShOrd+1)^2; % Total no. of Spherical Harmonics = (Order + 1)^2 
nShCirc = 2*maxShOrd + 1; % No. of spherical harmonics in horizontal plane 

idc_circ = zeros(nShCirc,1);
idc_circ(1) = 1; %ord 0 component

% Generates the indices to select the spherical harmonics which are only
% affected by azimuth (outer few in pyramid) 
% nShCirc = 37
for ord=1:maxShOrd
    idc_circ(1+(ord-1)*2 + [1 2]) =  1+ord^2 + ord + ord*[-1 1];
end

nAzMeasure = length(measure_grid_az_deg);
nAzInterp = length(interp_grid_az_deg);

% Inclination of Measurements: 
measure_grid_inc_deg = 90*ones(size(measure_grid_az_deg));
interp_grid_inc_deg = 90*ones(size(interp_grid_az_deg));


% Find the basis spherical harmonics functions evaluated at specified
% azimuths and inclinations: 

% Output: Spherical harmonics for each direction (nAzMeasure x nSH matrix: i.e 36 x 361 matrix) 
Ymeasure = sphBasis(deg2rad(measure_grid_az_deg),...
                    deg2rad(measure_grid_inc_deg),...
                    maxShOrd); %[nAzMeasure nSH]

% Limit to only the SHs that characterise the horizontal plane,
% output Ymeasure is a 36 x 37 matrix 
Ymeasure = Ymeasure(:,idc_circ); %[nAzMeasure nShCirc] 

% Find the basis spherical harmonic functions evaluated at specified azimuths and inclinations for
% the interpolation grid: 
Yinterp = sphBasis(deg2rad(interp_grid_az_deg),...
                    deg2rad(interp_grid_inc_deg),...
                    maxShOrd); %[nAzInterp nSH]
                
Yinterp = Yinterp(:,idc_circ); %[nAzInterp nShCirc]
                                 
nSamples = size(ir_measure,1);
nFFT = nSamples;

% Calculate the DFT of the impulse responses: 
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

% The inverse matrix maps from observed values to SH coefficients
% Ymeasure is the SH basis vectors - basically the SH coefficients 
Yinv = pinv(Ymeasure); % Obtain pseudoinverse of SH basis vectors 

%% do the transformation to SH domain
% Concentrate on just one microphone signal
% Rearranging data to plot azimuth against frequency
measuredData = permute(tf_measure(:,irefchan,:),[3 1 2]); %[nAzMeasure nFreq] 

% Calculate the estimated SH cofficients (i.e weights) 
est_fnm = Yinv * measuredData;

% Reconstruct
% Summation of SH coefficients with SH basis vectors to reconstruct
% function in frequency domain
reconstructedData = Ymeasure * est_fnm;
% Convert back from frequency into time domain: 
ir_reconstructed = irfft(permute(reconstructedData,[2 3 1]),nFFT,1); %[nSamples,1,nAzMeasure]

% Interpolate
% Use SH basis functions defined at interpolation grid and compute using
% SH coefficients (weights) calculated earlier 
interpolatedData = Yinterp * est_fnm;
ir_interpolated = irfft(permute(interpolatedData,[2 3 1]),nFFT,1); %[nSamples,1,nAzInterp]

%% plot the measured impulse responses and the reconstructed versions
figure;
plot(squeeze(ir_measure(:,irefchan,:)))
hold all;
plot(squeeze(ir_reconstructed(:,1,:)),':') % Reconstructed values are dotted lines 
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
plot(squeeze(ir_interpolated(:,1,:)),'--') % Interpolated values are dashed lines 
legend(num2str([interp_grid_az_deg;interp_grid_az_deg]))
title('Ground Truth Impulse Responses and Interpolated Versions') 
% hide all lines so that pairs can be turned on for comparison in plot browser window
lh = get(gca,'children');
set(lh,'visible','off')
set(gcf,'windowstyle','docked')
% Dotted lines are the interpolated versions
