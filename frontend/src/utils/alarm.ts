// Simple Web Audio API Siren Synthesizer

class AlarmSystem {
  private audioCtx: AudioContext | null = null;
  private oscillator: OscillatorNode | null = null;
  private gainNode: GainNode | null = null;
  private isPlaying = false;
  private intervalId: number | null = null;

  init() {
    if (!this.audioCtx) {
      this.audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
    }
  }

  play() {
    if (this.isPlaying) return;
    this.init();
    if (!this.audioCtx) return;

    this.isPlaying = true;
    
    // Create an oscillator for a synthetic siren sound
    this.oscillator = this.audioCtx.createOscillator();
    this.gainNode = this.audioCtx.createGain();
    
    this.oscillator.type = 'square';
    this.oscillator.connect(this.gainNode);
    this.gainNode.connect(this.audioCtx.destination);
    
    // Siren effect modulation
    this.gainNode.gain.setValueAtTime(0.1, this.audioCtx.currentTime); // keep volume low
    
    this.oscillator.frequency.setValueAtTime(400, this.audioCtx.currentTime);
    
    // Modulate frequency to sound like an alarm
    let high = true;
    this.intervalId = window.setInterval(() => {
      if (this.oscillator && this.audioCtx) {
        this.oscillator.frequency.setValueAtTime(high ? 600 : 400, this.audioCtx.currentTime);
        high = !high;
      }
    }, 500);

    this.oscillator.start();
  }

  stop() {
    if (!this.isPlaying) return;
    
    if (this.intervalId) {
      window.clearInterval(this.intervalId);
      this.intervalId = null;
    }
    
    if (this.oscillator) {
      this.oscillator.stop();
      this.oscillator.disconnect();
      this.oscillator = null;
    }
    
    if (this.gainNode) {
      this.gainNode.disconnect();
      this.gainNode = null;
    }
    
    this.isPlaying = false;
  }
}

export const systemAlarm = new AlarmSystem();
