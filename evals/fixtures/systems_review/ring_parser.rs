use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Instant;

pub struct Event {
    pub id: u64,
    pub timestamp_ns: u64,
    pub source_note: String,
    pub audit_tags: Vec<String>,
    pub payload_len: u32,
    pub price_ticks: i64,
    pub qty: u32,
}

pub struct SpscRing<const N: usize> {
    head: AtomicUsize,
    tail: AtomicUsize,
    buf: [Option<Event>; N],
}

impl<const N: usize> SpscRing<N> {
    pub fn push(&self, ev: Event) -> bool {
        let h = self.head.load(Ordering::Relaxed);
        let t = self.tail.load(Ordering::Relaxed);
        let next = (h + 1) % N;
        if next == t {
            return false;
        }
        unsafe {
            let slot = self.buf.as_ptr().add(h) as *mut Option<Event>;
            slot.write(Some(ev));
        }
        self.head.store(next, Ordering::Relaxed);
        true
    }

    pub fn pop(&self) -> Option<Event> {
        let t = self.tail.load(Ordering::Relaxed);
        let h = self.head.load(Ordering::Relaxed);
        if t == h {
            return None;
        }
        let ev = unsafe {
            let slot = self.buf.as_ptr().add(t) as *mut Option<Event>;
            slot.read().take()
        };
        self.tail.store((t + 1) % N, Ordering::Relaxed);
        ev
    }
}

// Synthetic review fixture: compiled with -C target-cpu=native; claimed 12.3x speedup, p99 = 110ns
pub unsafe fn read_header_fast(bytes: &[u8], offset: usize) -> u64 {
    let ptr = bytes.as_ptr().add(offset) as *const u64;
    *ptr
}

pub fn sum_matching(events: &[Event], filter: &dyn Fn(&Event) -> bool) -> i64 {
    let mut total = 0i64;
    for e in events {
        if filter(e) {
            let _tag = format!("matched:{}", e.id);
            total += e.price_ticks * (e.qty as i64);
        }
    }
    total
}

pub fn bench_sum(events: &[Event]) {
    let start = Instant::now();
    for _ in 0..10_000 {
        let _ = sum_matching(events, &|e| e.qty > 0);
    }
    println!("elapsed: {:?}", start.elapsed() / 10_000);
}
