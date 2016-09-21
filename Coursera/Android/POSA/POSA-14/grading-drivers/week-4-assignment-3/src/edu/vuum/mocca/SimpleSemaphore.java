package edu.vuum.mocca;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

/**
 * @class SimpleSemaphore
 *
 * @brief This class provides a simple counting semaphore
 *        implementation using Java a ReentrantLock and a
 *        ConditionObject.  It must implement both "Fair" and
 *        "NonFair" semaphore semantics, just liked Java Semaphores. 
 */
public class SimpleSemaphore {

    /**
     * Define a ReentrantLock to protect the critical section.
     */
    // TODO - you fill in here
    
    private ReentrantLock mReentrantLock = null;

    /**
     * Define a ConditionObject to wait while the number of
     * permits is 0.
     */

    // TODO - you fill in here
    
    private Condition mAllPermitsTaken = null;
    
    /**
     * Define a count of the number of available permits.
     */

    // TODO - you fill in here
    private volatile int mNumPermits = 0;


    /**
     * Constructor initialize the data members.  
     */
    public SimpleSemaphore (int permits,
                            boolean fair)
    { 
        // TODO - you fill in here
    	
    	mReentrantLock = new ReentrantLock(fair) ;
    	mAllPermitsTaken = mReentrantLock.newCondition();
    	mReentrantLock.lock();
    	this.mNumPermits = permits;
    	mReentrantLock.unlock();
    }

    /**
     * Acquire one permit from the semaphore in a manner that can
     * be interrupted.
     */
    public void acquire() throws InterruptedException {
        // TODO - you fill in here
    	
    	mReentrantLock.lockInterruptibly();
    	try {
    		while (mNumPermits == 0) {
    			mAllPermitsTaken.await();
    		}	
    		mNumPermits -- ;
    		
    	} catch(java.lang.InterruptedException e) {
    		System.out.println("Caught exception" + e);
    	}
    	finally {
    			mReentrantLock.unlock();
    		}
    }

    /**
     * Acquire one permit from the semaphore in a manner that
     * cannot be interrupted.
     */
    public void acquireUninterruptibly() {
        // TODO - you fill in here
    	
    	mReentrantLock.lock();
    	try {
    		while (mNumPermits == 0) {
    			mAllPermitsTaken.awaitUninterruptibly();
    		}	
    		mNumPermits -- ;
    		
    	} finally {
    			mReentrantLock.unlock();
    		}
    }

    /**
     * Return one permit to the semaphore.
     */
    void release() {
        // TODO - you fill in here
    	
    	mReentrantLock.lock();
    	try {	
    		mNumPermits ++ ;
    		mAllPermitsTaken.signalAll();		
    	} finally {
    			mReentrantLock.unlock();
    		}
    }

    /**
     * Return the number of permits available.
     */
    public int availablePermits() {
        // TODO - you fill in here by changing null to the appropriate
        // return value.
    	
    	mReentrantLock.lock();
    	try {
    			return mNumPermits;
    	} finally {
    		mReentrantLock.unlock();
    	}
    }
}

