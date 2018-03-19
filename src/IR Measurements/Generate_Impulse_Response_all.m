% Generate Impulse Responses from all directions from Recorded Sweep 
addpath(genpath('/home/bngzl/Documents/Final Year Project/final_year_project/src/audio'))

% Setup: 
in.signal_opts.settings = {20, 24000, 0.6, 48000};
in.gain_opts.gain = 1;
nDirections = 72; % From azimuth 0 to azimuth 355) 

ir_all = zeros(615589, 5, nDirections);

for i = 1:(nDirections)
    index = i-1; 
    audioFileName = sprintf('/home/bngzl/Documents/Final Year Project/final_year_project/src/audio/rvrb_sweep_azimuth_%d.wav', index); 
    [in.rawResponse in.fs] = audioread(audioFileName); 
    ir = recover_RIR_from_recorded_sweep(in); 
    ir_all(:,:,i) = ir; 
end

% https://uk.mathworks.com/matlabcentral/answers/57446-faq-how-can-i-process-a-sequence-of-files
