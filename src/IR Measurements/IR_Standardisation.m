% Script to realign and crop all .wav files to remove reverb 

% Initialisation: 
addpath(genpath('/home/bngzl/Documents/Final Year Project/final_year_project/src/audio/rvrb_sweep_909b'))
addpath(genpath('Impulse Response Conversion'))

clear all; 
in.signal_opts.settings = {20, 24000, 0.6, 48000};
in.gain_opts.gain = 1;

nDirections = 71; 

ir_standardised = zeros(501, 4, nDirections);

for i = 1:(nDirections)
    index = i-1; 
    audioFileName = sprintf('/home/bngzl/Documents/Final Year Project/final_year_project/src/audio/rvrb_sweep_909b/rvrb_sweep_azimuth_%d.wav', index); 
    [in.rawResponse in.fs] = audioread(audioFileName);
    ir = recover_RIR_from_recorded_sweep(in); 
    
    % Align signal according to Loopback delay 
    loopback_channel = ir(:,5); 
    [~, x_align] = max(loopback_channel); % Find sample with largest response 
    
    % Comment out once figured where to trim reverb signal 
%     ir_aligned = ir(x_align+1:x_align+501,1:4); % 300 is arbitrary to ensure arrays are same sized
%     figure;
%     plot(20*log10(abs(ir_aligned)))
    % plot(ir_aligned) 
    
    % Use this to generate .mat data:
    ir_standardised(:,:,i) = ir(x_align+1:x_align+501,1:4); % after loopback (x_align+1) to end 
    
end
save ('ir_standardised_horizontal_plane_909b.mat', 'ir_standardised'); 