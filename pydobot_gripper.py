from pydobot import Dobot
import time

class DobotPalletizer:
    def __init__(self, port="COM12", safe_height=50, rotation=0):
        """Initialize Dobot connection and parameters"""
        self.port = port
        self.safe_height = safe_height
        self.rotation = rotation
        self.device = None
        
        # Block positions (pick and drop coordinates)
        self.blocks = [
            {"pick": {"x": 252.87, "y": -49.02, "z": -14.23}, 
             "drop": {"x": 243.327, "y": 49.75, "z": -15.83, "r": -10}},
            {"pick": {"x": 245.92, "y": 6.15, "z": -14.30}, 
             "drop": {"x": 242.36, "y": 99.21, "z": -15.52, "r": 2.16}},
            {"pick": {"x": 316.89, "y": -40.12, "z": -14.31}, 
             "drop": {"x": 300.19, "y": 53.44, "z": -9.58, "r": -11.53}},
            {"pick": {"x": 306.52, "y": 15.33, "z": -14.78}, 
             "drop": {"x": 297.70, "y": 109.51, "z": -12.93, "r": -1.43}}
        ]
        
        # Return positions (reverse of blocks for returning to original positions)
        self.return_blocks = [
            {"pick": {"x": 243.327, "y": 49.75, "z": -15.83, "r": -10}, 
             "drop": {"x": 252.87, "y": -49.02, "z": -14.23}},
            {"pick": {"x": 242.36, "y": 99.21, "z": -15.52, "r": 2.16}, 
             "drop": {"x": 245.92, "y": 6.15, "z": -14.30}},
            {"pick": {"x": 300.19, "y": 53.44, "z": -9.58, "r": -11.53}, 
             "drop": {"x": 316.89, "y": -40.12, "z": -14.31}},
            {"pick": {"x": 297.70, "y": 109.51, "z": -12.93, "r": -1.43}, 
             "drop": {"x": 306.52, "y": 15.33, "z": -14.78}}
        ]
        
        self.connect()
    
    def connect(self):
        """Connect to Dobot device"""
        try:
            print(f"Connecting to Dobot on {self.port}...")
            self.device = Dobot(port=self.port)
            self.device.grip(False)  # Ensure gripper is off
            print("Successfully connected to Dobot!")
        except Exception as e:
            print(f"Connection failed: {e}")
            raise
    
    def move_block(self, pick_pos, drop_pos, block_num):
        """Move a single block from pick to drop position"""
        print(f"\nHandling Block {block_num}:")
        
        # Extract coordinates with proper rotation handling
        pick_x, pick_y, pick_z = pick_pos["x"], pick_pos["y"], pick_pos["z"]
        pick_r = pick_pos.get("r", self.rotation)  # Use pick rotation if available
        drop_x, drop_y, drop_z = drop_pos["x"], drop_pos["y"], drop_pos["z"]
        drop_r = drop_pos.get("r", self.rotation)  # Use drop rotation if available
        
        try:
            # Move above pick point
            self.device.move_to(pick_x, pick_y, self.safe_height, pick_r)
            time.sleep(1)
            
            # Move down to pick
            self.device.move_to(pick_x, pick_y, pick_z, pick_r)
            time.sleep(1)
            
            # Enable suction/grip
            print("  Picking up block...")
            self.device.grip(True)
            time.sleep(2)
            
            # Lift up
            self.device.move_to(pick_x, pick_y, self.safe_height, pick_r)
            time.sleep(1)
            
            # Move above drop point
            self.device.move_to(drop_x, drop_y, self.safe_height, drop_r)
            time.sleep(1)
            
            # Move down to drop
            self.device.move_to(drop_x, drop_y, drop_z, drop_r)
            time.sleep(1)
            
            # Disable suction/grip
            print("  Dropping block...")
            self.device.grip(False)
            time.sleep(2)
            
            # Lift up after drop
            self.device.move_to(drop_x, drop_y, self.safe_height, drop_r)
            time.sleep(1)
            
            print(f"  Block {block_num} handled successfully!")
            return True
            
        except Exception as e:
            print(f"  Error handling block {block_num}: {e}")
            self.device.grip(False)  # Ensure grip is released
            return False
    
    def transfer_blocks(self):
        """Transfer all blocks from source to destination"""
        print("=== Starting Block Transfer ===")
        successful_transfers = 0
        
        for i, block in enumerate(self.blocks, start=1):
            if self.move_block(block["pick"], block["drop"], i):
                successful_transfers += 1
            else:
                print(f"Failed to transfer block {i}")
        
        print(f"\n=== Transfer Complete: {successful_transfers}/{len(self.blocks)} blocks transferred ===")
        return successful_transfers
    
    def return_blocks(self):
        """Return all blocks to their original positions"""
        print("\n=== Returning Blocks to Original Positions ===")
        successful_returns = 0
        
        for i, block in enumerate(self.return_blocks, start=1):
            if self.move_block(block["pick"], block["drop"], i):
                successful_returns += 1
            else:
                print(f"Failed to return block {i}")
        
        print(f"\n=== Return Complete: {successful_returns}/{len(self.return_blocks)} blocks returned ===")
        return successful_returns
    
    def run_complete_cycle(self):
        """Run complete palletization cycle (transfer + return)"""
        print("=== DOBOT PALLETIZATION CYCLE ===")
        start_time = time.time()
        
        try:
            # Transfer blocks
            transferred = self.transfer_blocks()
            
            if transferred > 0:
                # Pause between operations
                print("\nPausing for 3 seconds before return operation...")
                time.sleep(3)
                
                # Return blocks
                returned = self.return_blocks()
                
                # Results
                total_time = time.time() - start_time
                print(f"\n=== CYCLE RESULTS ===")
                print(f"Blocks transferred: {transferred}/{len(self.blocks)}")
                print(f"Blocks returned: {returned}/{len(self.return_blocks)}")
                print(f"Total cycle time: {total_time:.2f} seconds")
                
                return {"transferred": transferred, "returned": returned, "time": total_time}
            else:
                print("No blocks were transferred successfully. Skipping return operation.")
                return None
                
        except Exception as e:
            print(f"Error during cycle: {e}")
            self.emergency_stop()
            return None
    
    def emergency_stop(self):
        """Emergency stop - release grip and stop operations"""
        print("\n!!! EMERGENCY STOP !!!")
        try:
            if self.device:
                self.device.grip(False)
                print("Grip released")
        except Exception as e:
            print(f"Error during emergency stop: {e}")
    
    def disconnect(self):
        """Safely disconnect from Dobot"""
        try:
            if self.device:
                print("Disconnecting from Dobot...")
                self.device.grip(False)  # Ensure grip is off
                self.device.close()
                self.device = None
                print("Dobot disconnected successfully")
        except Exception as e:
            print(f"Error during disconnect: {e}")

def main():
    """Main execution function"""
    palletizer = None
    
    try:
        # Initialize palletizer (change COM port as needed)
        palletizer = DobotPalletizer(port="COM12")
        
        # Run complete cycle
        results = palletizer.run_complete_cycle()
        
        if results:
            print(f"\n=== SUCCESS ===")
            print("All operations completed successfully!")
        else:
            print("\n=== FAILED ===")
            print("Operations were not completed successfully")
            
    except KeyboardInterrupt:
        print("\n\nKeyboard interrupt detected...")
        if palletizer:
            palletizer.emergency_stop()
        print("Program interrupted safely")
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        if palletizer:
            palletizer.emergency_stop()
            
    finally:
        # Always disconnect
        if palletizer:
            palletizer.disconnect()
        print("Program terminated")

if __name__ == "__main__":
    main()