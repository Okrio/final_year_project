% example of interpolation using the Spherical Harmonic (SH) domain using
% impulse responses for microphones mounted on the surface of an ideal
% sphere
restoredefaultpath
addpath(genpath('dependencies'))

fs = 48000;


% Could do it for microphones in free space, but their responses aren't very interesting!
% nSensors = 4;
% sensorSpacing = 0.025;
% ema = FreeField_20180202_01_ULA_configurable(nSensors,sensorSpacing);

% Do it for a rigid sphere with radius 4.2 cm, rotated so that sensor 2 is
% on the horizontal plane and aligned with the x axis
ema = RigidSphere_20171114_01_ideal_em32();
ema.setPoseRollPitchYawDegrees(0,0,-32);
ema.prepareData(fs);

measure_grid_az_deg = (0:10:350).';
interp_grid_az_deg = (5:10:355).';

% dimension of SH representation
maxShOrd = 18;
nSh = (maxShOrd+1)^2;
nShCirc = 2*maxShOrd + 1;

idc_circ = zeros(nShCirc,1);
idc_circ(1) = 1; %ord 0 component
for ord=1:maxShOrd
    idc_circ(1+(ord-1)*2 + [1 2]) =  1+ord^2 + ord + ord*[-1 1];
end



nAzMeasure = length(measure_grid_az_deg);
nAzInterp = length(interp_grid_az_deg);


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


ir_measure = ema.getImpulseResponseForSrc(deg2rad(measure_grid_az_deg),...
                                          deg2rad(measure_grid_inc_deg));
                                      
ir_interp_gt = ema.getImpulseResponseForSrc(deg2rad(interp_grid_az_deg),...
                                          deg2rad(interp_grid_inc_deg));
                                    
nSamples = size(ir_measure,1);
nFFT = nSamples;
tf_measure = rfft(ir_measure,nFFT,1); %[nFreq nSensors, nAzMeasure]
nFreq = size(tf_measure,1);
fscale = (0:nFreq-1).' * (fs/nFFT);

%% quick plot of data to check it makes sense
irefchan = 2; %with rotation applied, this sensor is aligned with x axis
figure;plot(squeeze(ir_measure(:,irefchan,:)))
legend(num2str(measure_grid_az_deg))
title('Quick Plot') 
%first arrival should be from 0 degrees

% the inverse matrix maps from observed values to SH coefficients
Yinv = pinv(Ymeasure);

%% do the transformation to SH domain
% concentrate on just one microphone signal
measuredData = permute(tf_measure(:,irefchan,:),[3 1 2]); %[nAzMeasure nFreq]

% get the estimated SH cofficients
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

%% plot the ground interpolated impulse responses and the interpolated versions
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
