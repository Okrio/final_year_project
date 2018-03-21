% Script to realign and crop all .wav files to remove reverb 

% Initialisation: 
addpath(genpath('/home/bngzl/Documents/Final Year Project/final_year_project/src/audio'))
addpath(genpath('Impulse Response Conversion'))

clear all; 
in.signal_opts.settings = {20, 24000, 0.6, 48000};
in.gain_opts.gain = 1;

nDirections = 71; 

ir_standardised = zeros(180, 4, nDirections);

for i = 1:(nDirections)
    index = i-1; 
    audioFileName = sprintf('/home/bngzl/Documents/Final Year Project/final_year_project/src/audio/rvrb_sweep_azimuth_%d.wav', index); 
    [in.rawResponse in.fs] = audioread(audioFileName);
    ir = recover_RIR_from_recorded_sweep(in); 
    
    % Align signal according to Loopback delay 
    loopback_channel = ir(:,5); 
    [~, x_align] = max(loopback_channel); % Find sample with largest response 
    
    ir_standardised(:,:,i) = ir(x_align+1:x_align+180,1:4); % after loopback (x_align+1) to end 
    
    
    %figure;
    %plot(ir_aligned) 
    %plot(20*log10(abs(ir_aligned)))
end
save ('ir_standardised.mat', 'ir_standardised'); 