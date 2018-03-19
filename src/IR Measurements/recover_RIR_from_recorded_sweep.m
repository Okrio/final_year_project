function [ir, full_response] = recover_RIR_from_recorded_sweep( in )
fs = in.fs;

rawResponse = in.rawResponse;
inv_gain = 1/in.gain_opts.gain;


[f_start,f_end,sec_per_octave,~] = deal(in.signal_opts.settings{:});
[sweep, ~, scale_factor, inv_sweep] = generateSineSweep(f_start, f_end, sec_per_octave, fs);

nfft = length(rawResponse) + length(inv_sweep) - 1;
fft_inv = fft(inv_sweep,nfft);
fft_raw = fft(double(rawResponse),nfft);
%correct op gain and the scaling required for conv(sweep, inv_sweep) to give
%unit impulse
full_response =  inv_gain * scale_factor * real(ifft( bsxfun(@times,fft_raw,fft_inv)));
ir = full_response(length(sweep):end,:); %extract the linear part

