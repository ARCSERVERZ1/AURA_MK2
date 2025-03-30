from pytapo import Tapo
import asyncio
import kasa


async def trigger_snapshot():
    email = "baswasanjaybabu@gmail.com"
    password = "tplink@119"

    # Initialize Tapo API with credentials
    tapo = Tapo(email, password)

    # Fetch the list of devices
    devices = await tapo.devices()
    camera = devices[0]  # Assuming the first device is the camera

    # Trigger a snapshot
    snapshot = await camera.take_snapshot()

    # Save the snapshot to a file
    with open("snapshot.jpg", "wb") as file:
        file.write(snapshot)
    print("Snapshot saved!")

# Call the async function
asyncio.run(trigger_snapshot())
