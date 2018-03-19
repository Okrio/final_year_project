% Recovering Impulse Response from Recorded Sweep 
[in.rawResponse in.fs] = audioread('/home/bngzl/Documents/Final Year Project/final_year_project/src/audio/rvrb_sweep_azimuth_0.wav');
in.signal_opts.settings = {20, 24000, 0.6, 48000}
in.gain_opts.gain =1
ir = recover_RIR_from_recorded_sweep(in); 
figure; plot(ir) 

hold
[in.rawResponse in.fs] = audioread('/home/bngzl/Documents/Final Year Project/final_year_project/src/audio/rvrb_sweep_azimuth_37.wav');
in.signal_opts.settings = {20, 24000, 0.6, 48000}
in.gain_opts.gain =1
ir = recover_RIR_from_recorded_sweep(in); 
figure; plot(ir) 