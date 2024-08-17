//Components
import Header from "../Components/Header"
import ComplaintTab from './ComplaintTab'
import ViewPort from './ViewPort'

export default function dashboard() {
    return (
      <div>
        <Header />
        <div>
          <ComplaintTab />
          <ViewPort />
        </div>
      </div>
    );
}