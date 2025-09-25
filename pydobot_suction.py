from pydobot import Dobot
import time

class DobotPalletizer:
    def __init__(self, port="/dev/ttyACM0", safe_height=50, rotation=0):
        """Initialize Dobot connection and parameters"""
        self.port = port
        self.safe_height = safe_height
        self.rotation = rotation
        self.device = None
        
        # Block positions (pick and drop coordinates)
        self.blocks = [
            {"pick": {"x": 288.34, "y": -41.49, "z": -41.33}, 
             "drop": {"x": 281.02, "y": 93.43, "z": -40.75}},
            {"pick": {"x": 286.20, "y": 20.33, "z": -41.25}, 
             "drop": {"x": 277.09, "y": 154.90, "z": -40.51}},
            {"pick": {"x": 346.69, "y": -38.67, "z": -42.27}, 
             "drop": {"x": 338.69, "y": 98.97, "z": -41.70}},
            {"pick": {"x": 344.29, "y": 22.79, "z": -42.85}, 
             "drop": {"x": 332.51, "y": 158.89, "z": -42.41}}
        ]
        
        self.connect()
    
    def connect(self):
        """Connect to Dobot device"""
        try:
            print(f"Connecting to Dobot on {self.port}...")
            self.device = Dobot(port=self.port)
            self.device.suck(False)  # Ensure suction is off
            print("Successfully connected to Dobot!")
        except Exception as e:
            print(f"Connection failed: {e}")
            raise
    
    def move_block(self, pick_pos, drop_pos, block_num, operation="transfer"):
        """Move a single block from pick to drop position"""
        print(f"\nHandling Block {block_num} ({operation}):")
        
        # Extract coordinates
        pick_x, pick_y, pick_z = pick_pos["x"], pick_pos["y"], pick_pos["z"]
        drop_x, drop_y, drop_z = drop_pos["x"], drop_pos["y"], drop_pos["z"]
        
        try:
            # Move above pick point
            print(f"  Moving above pick point...")
            self.device.move_to(pick_x, pick_y, self.safe_height, self.rotation)
            time.sleep(1)
            
            # Move down to pick
            print(f"  Moving down to pick...")
            self.device.move_to(pick_x, pick_y, pick_z, self.rotation)
            time.sleep(1)
            
            # Enable suction
            print("  Picking up block...")
            self.device.suck(True)
            time.sleep(2)
            
            # Lift up
            print(f"  Lifting block...")
            self.device.move_to(pick_x, pick_y, self.safe_height, self.rotation)
            time.sleep(1)
            
            # Move above drop point
            print(f"  Moving above drop point...")
            self.device.move_to(drop_x, drop_y, self.safe_height, self.rotation)
            time.sleep(1)
            
            # Move down to drop
            print(f"  Moving down to drop...")
            self.device.move_to(drop_x, drop_y, drop_z, self.rotation)
            time.sleep(1)
            
            # Disable suction
            print("  Dropping block...")
            self.device.suck(False)
            time.sleep(2)
            
            # Lift up after drop
            print(f"  Lifting after drop...")
            self.device.move_to(drop_x, drop_y, self.safe_height, self.rotation)
            time.sleep(1)
            
            print(f"  Block {block_num} {operation} completed successfully!")
            return True
            
        except Exception as e:
            print(f"  Error handling block {block_num}: {e}")
            try:
                self.device.suck(False)  # Ensure suction is released
            except:
                pass
            return False
    
    def transfer_blocks(self):
        """Transfer all blocks from source to destination"""
        print("=== Starting Block Transfer ===")
        successful_transfers = 0
        
        for i, block in enumerate(self.blocks, start=1):
            if self.move_block(block["pick"], block["drop"], i, "transfer"):
                successful_transfers += 1
            else:
                print(f"Failed to transfer block {i}")
        
        print(f"\n=== Transfer Complete: {successful_transfers}/{len(self.blocks)} blocks transferred ===")
        return successful_transfers
    
    def return_blocks(self):
        """Return all blocks to their original positions"""
        print("\n=== Returning Blocks to Original Positions ===")
        successful_returns = 0
        
        for i, block in enumerate(self.blocks, start=1):
            # For return operation: pick from drop position, drop at pick position
            if self.move_block(block["drop"], block["pick"], i, "return"):
                successful_returns += 1
            else:
                print(f"Failed to return block {i}")
        
        print(f"\n=== Return Complete: {successful_returns}/{len(self.blocks)} blocks returned ===")
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
                print(f"Blocks returned: {returned}/{len(self.blocks)}")
                print(f"Total cycle time: {total_time:.2f} seconds")
                
                return {"transferred": transferred, "returned": returned, "time": total_time}
            else:
                print("No blocks were transferred successfully. Skipping return operation.")
                return None
                
        except Exception as e:
            print(f"Error during cycle: {e}")
            self.emergency_stop()
            return None
    
    def run_transfer_only(self):
        """Run only the transfer operation (no return)"""
        print("=== DOBOT TRANSFER OPERATION ===")
        start_time = time.time()
        
        try:
            transferred = self.transfer_blocks()
            transfer_time = time.time() - start_time
            
            print(f"\n=== TRANSFER RESULTS ===")
            print(f"Blocks transferred: {transferred}/{len(self.blocks)}")
            print(f"Transfer time: {transfer_time:.2f} seconds")
            
            return {"transferred": transferred, "time": transfer_time}
            
        except Exception as e:
            print(f"Error during transfer: {e}")
            self.emergency_stop()
            return None
    
    def run_return_only(self):
        """Run only the return operation (assumes blocks are already transferred)"""
        print("=== DOBOT RETURN OPERATION ===")
        start_time = time.time()
        
        try:
            returned = self.return_blocks()
            return_time = time.time() - start_time
            
            print(f"\n=== RETURN RESULTS ===")
            print(f"Blocks returned: {returned}/{len(self.blocks)}")
            print(f"Return time: {return_time:.2f} seconds")
            
            return {"returned": returned, "time": return_time}
            
        except Exception as e:
            print(f"Error during return: {e}")
            self.emergency_stop()
            return None
    
    def emergency_stop(self):
        """Emergency stop - release suction and stop operations"""
        print("\n!!! EMERGENCY STOP !!!")
        try:
            if self.device:
                self.device.suck(False)
                print("Suction released")
        except Exception as e:
            print(f"Error during emergency stop: {e}")
    
    def go_to_safe_position(self):
        """Move to a safe position"""
        try:
            print("Moving to safe position...")
            # Move to center position at safe height
            self.device.move_to(300, 0, self.safe_height, 0)
            time.sleep(2)
            print("Safe position reached")
            return True
        except Exception as e:
            print(f"Error moving to safe position: {e}")
            return False
    
    def disconnect(self):
        """Safely disconnect from Dobot"""
        try:
            if self.device:
                print("Disconnecting from Dobot...")
                self.device.suck(False)  # Ensure suction is off
                self.go_to_safe_position()  # Move to safe position
                self.device.close()
                self.device = None
                print("Dobot disconnected successfully")
        except Exception as e:
            print(f"Error during disconnect: {e}")

def main():
    """Main execution function"""
    palletizer = None
    
    try:
        # Initialize palletizer
        palletizer = DobotPalletizer(port="/dev/ttyACM0")
        
        # Menu for operation selection
        print("\n=== OPERATION MENU ===")
        print("1. Complete cycle (transfer + return)")
        print("2. Transfer only")
        print("3. Return only")
        choice = input("Select operation (1-3): ").strip()
        
        if choice == "1":
            results = palletizer.run_complete_cycle()
        elif choice == "2":
            results = palletizer.run_transfer_only()
        elif choice == "3":
            results = palletizer.run_return_only()
        else:
            print("Invalid choice. Running complete cycle...")
            results = palletizer.run_complete_cycle()
        
        if results:
            print(f"\n=== SUCCESS ===")
            print("Operations completed successfully!")
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